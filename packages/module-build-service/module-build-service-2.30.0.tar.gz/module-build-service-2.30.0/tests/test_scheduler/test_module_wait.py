# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
import mock
from mock import patch
import module_build_service.messaging
import module_build_service.scheduler.handlers.modules
import os
import koji
import pytest
from tests import conf, scheduler_init_data, read_staged_data
import module_build_service.resolver
from module_build_service import build_logs, Modulemd
from module_build_service.utils.general import load_mmd
from module_build_service.models import ComponentBuild, ModuleBuild

base_dir = os.path.dirname(os.path.dirname(__file__))


class TestModuleWait:
    def setup_method(self, test_method):
        self.config = conf
        self.session = mock.Mock()
        self.fn = module_build_service.scheduler.handlers.modules.wait

    def teardown_method(self, test_method):
        try:
            with module_build_service.models.make_db_session(conf) as db_session:
                path = build_logs.path(db_session, 1)
            os.remove(path)
        except Exception:
            pass

    @patch("module_build_service.builder.GenericBuilder.create_from_module")
    @patch("module_build_service.models.ModuleBuild.from_module_event")
    def test_init_basic(self, from_module_event, create_builder):
        builder = mock.Mock()
        builder.get_disttag_srpm.return_value = "some srpm disttag"
        builder.build.return_value = 1234, 1, "", None
        builder.module_build_tag = {"name": "some-tag-build"}
        create_builder.return_value = builder
        mocked_module_build = mock.Mock()
        mocked_module_build.name = "foo"
        mocked_module_build.stream = "stream"
        mocked_module_build.version = "1"
        mocked_module_build.context = "1234567"
        mocked_module_build.state = 1
        mocked_module_build.id = 1
        mocked_module_build.json.return_value = {
            "name": "foo",
            "stream": "1",
            "version": 1,
            "state": "some state",
            "id": 1,
        }
        mocked_module_build.id = 1
        mocked_module_build.mmd.return_value = load_mmd(read_staged_data("formatted_testmodule"))
        mocked_module_build.component_builds = []

        from_module_event.return_value = mocked_module_build

        msg = module_build_service.messaging.MBSModule(
            msg_id=None, module_build_id=1, module_build_state="some state")
        with patch("module_build_service.resolver.GenericResolver.create"):
            self.fn(config=self.config, db_session=self.session, msg=msg)

    @patch(
        "module_build_service.builder.GenericBuilder.default_buildroot_groups",
        return_value={"build": [], "srpm-build": []},
    )
    @patch("module_build_service.builder.GenericBuilder.create_from_module")
    @patch("module_build_service.resolver.DBResolver")
    @patch("module_build_service.resolver.GenericResolver")
    def test_new_repo_called_when_macros_reused(
        self, generic_resolver, resolver, create_builder, dbg, db_session
    ):
        """
        Test that newRepo is called when module-build-macros build is reused.
        """
        scheduler_init_data(db_session)
        koji_session = mock.MagicMock()
        koji_session.newRepo.return_value = 123456

        builder = mock.MagicMock()
        builder.koji_session = koji_session
        builder.module_build_tag = {"name": "module-123-build"}
        builder.get_disttag_srpm.return_value = "some srpm disttag"
        builder.build.return_value = (
            1234,
            koji.BUILD_STATES["COMPLETE"],
            "",
            "module-build-macros-1-1",
        )
        create_builder.return_value = builder

        resolver = mock.MagicMock()
        resolver.backend = "db"
        resolver.get_module_tag.return_value = "module-testmodule-master-20170109091357"

        generic_resolver.create.return_value = resolver
        msg = module_build_service.messaging.MBSModule(
            msg_id=None, module_build_id=2, module_build_state="some state")

        module_build_service.scheduler.handlers.modules.wait(
            config=conf, db_session=db_session, msg=msg)

        koji_session.newRepo.assert_called_once_with("module-123-build")

        # When module-build-macros is reused, it still has to appear only
        # once in database.
        builds_count = db_session.query(ComponentBuild).filter_by(
            package="module-build-macros", module_id=2).count()
        assert builds_count == 1

    @patch(
        "module_build_service.builder.GenericBuilder.default_buildroot_groups",
        return_value={"build": [], "srpm-build": []},
    )
    @patch("module_build_service.builder.GenericBuilder.create_from_module")
    @patch("module_build_service.resolver.DBResolver")
    @patch("module_build_service.resolver.GenericResolver")
    def test_new_repo_not_called_when_macros_not_reused(
        self, generic_resolver, resolver, create_builder, dbg, db_session
    ):
        """
        Test that newRepo is called everytime for module-build-macros
        """
        scheduler_init_data(db_session)
        koji_session = mock.MagicMock()
        koji_session.newRepo.return_value = 123456

        builder = mock.MagicMock()
        builder.koji_session = koji_session
        builder.module_build_tag = {"name": "module-123-build"}
        builder.get_disttag_srpm.return_value = "some srpm disttag"
        builder.build.return_value = (
            1234,
            koji.BUILD_STATES["BUILDING"],
            "",
            "module-build-macros-1-1",
        )
        create_builder.return_value = builder

        resolver = mock.MagicMock()
        resolver.backend = "db"
        resolver.get_module_tag.return_value = "module-testmodule-master-20170109091357"

        generic_resolver.create.return_value = resolver
        msg = module_build_service.messaging.MBSModule(
            msg_id=None, module_build_id=2, module_build_state="some state")

        module_build_service.scheduler.handlers.modules.wait(
            config=conf, db_session=db_session, msg=msg)

        assert koji_session.newRepo.called

    @patch(
        "module_build_service.builder.GenericBuilder.default_buildroot_groups",
        return_value={"build": [], "srpm-build": []},
    )
    @patch("module_build_service.builder.GenericBuilder.create_from_module")
    @patch("module_build_service.resolver.DBResolver")
    @patch("module_build_service.resolver.GenericResolver")
    def test_set_cg_build_koji_tag_fallback_to_default(
        self, generic_resolver, resolver, create_builder, dbg, db_session
    ):
        """
        Test that build.cg_build_koji_tag fallbacks to default tag.
        """
        base_mmd = Modulemd.ModuleStreamV2.new("base-runtime", "f27")

        scheduler_init_data(db_session)
        koji_session = mock.MagicMock()
        koji_session.newRepo.return_value = 123456

        builder = mock.MagicMock()
        builder.koji_session = koji_session
        builder.module_build_tag = {"name": "module-123-build"}
        builder.get_disttag_srpm.return_value = "some srpm disttag"
        builder.build.return_value = (
            1234,
            koji.BUILD_STATES["BUILDING"],
            "",
            "module-build-macros-1-1",
        )
        create_builder.return_value = builder

        resolver = mock.MagicMock()
        resolver.backend = "db"
        resolver.get_module_tag.return_value = "module-testmodule-master-20170109091357"
        resolver.get_module_build_dependencies.return_value = {
            "module-bootstrap-tag": [base_mmd]
        }

        generic_resolver.create.return_value = resolver
        msg = module_build_service.messaging.MBSModule(
            msg_id=None, module_build_id=2, module_build_state="some state")

        module_build_service.scheduler.handlers.modules.wait(
            config=conf, db_session=db_session, msg=msg)

        module_build = ModuleBuild.get_by_id(db_session, 2)
        assert module_build.cg_build_koji_tag == "modular-updates-candidate"

    @pytest.mark.parametrize(
        "koji_cg_tag_build,expected_cg_koji_build_tag",
        [
            [True, "f27-modular-updates-candidate"],
            [False, None]
        ],
    )
    @patch(
        "module_build_service.builder.GenericBuilder.default_buildroot_groups",
        return_value={"build": [], "srpm-build": []},
    )
    @patch("module_build_service.builder.GenericBuilder.create_from_module")
    @patch("module_build_service.resolver.DBResolver")
    @patch("module_build_service.resolver.GenericResolver")
    @patch(
        "module_build_service.config.Config.base_module_names",
        new_callable=mock.PropertyMock,
        return_value=["base-runtime", "platform"],
    )
    def test_set_cg_build_koji_tag(
        self,
        cfg,
        generic_resolver,
        resolver,
        create_builder,
        dbg,
        koji_cg_tag_build,
        expected_cg_koji_build_tag,
        db_session,
    ):
        """
        Test that build.cg_build_koji_tag is set.
        """
        base_mmd = Modulemd.ModuleStreamV2.new("base-runtime", "f27")

        scheduler_init_data(db_session)
        koji_session = mock.MagicMock()
        koji_session.newRepo.return_value = 123456

        builder = mock.MagicMock()
        builder.koji_session = koji_session
        builder.module_build_tag = {"name": "module-123-build"}
        builder.get_disttag_srpm.return_value = "some srpm disttag"
        builder.build.return_value = (
            1234,
            koji.BUILD_STATES["BUILDING"],
            "",
            "module-build-macros-1-1",
        )
        create_builder.return_value = builder

        resolver = mock.MagicMock()
        resolver.backend = "db"
        resolver.get_module_tag.return_value = "module-testmodule-master-20170109091357"
        resolver.get_module_build_dependencies.return_value = {
            "module-bootstrap-tag": [base_mmd]
        }

        with patch.object(
            module_build_service.scheduler.handlers.modules.conf,
            "koji_cg_tag_build",
            new=koji_cg_tag_build,
        ):
            generic_resolver.create.return_value = resolver
            msg = module_build_service.messaging.MBSModule(
                msg_id=None, module_build_id=2, module_build_state="some state"
            )
            module_build_service.scheduler.handlers.modules.wait(
                config=conf, db_session=db_session, msg=msg
            )
            module_build = ModuleBuild.get_by_id(db_session, 2)
            assert module_build.cg_build_koji_tag == expected_cg_koji_build_tag
