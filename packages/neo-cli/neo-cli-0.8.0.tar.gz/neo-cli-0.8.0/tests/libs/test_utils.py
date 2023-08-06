import mock
import pathlib
import os
from os import path

import neo.libs.utils
from neo.libs import utils
from tests.fixtures import manifest


class TestLambdafunc:
    def test_isint(self):
        assert utils.isint(4) is True
        assert utils.isint(4.3) is False

    def test_isfloat(self):
        assert utils.isfloat(4.3) is True
        assert utils.isfloat("a") is False

    def test_list_dir(self):
        current_dir = path.abspath(path.dirname(__file__))
        assert any("test_utils.py" in d for d in utils.list_dir(current_dir))

    def test_read_file(self):
        current_dir = path.abspath(path.dirname(__file__))
        filename = "test_utils.py"
        assert "test_read_file(self):" in utils.read_file(f"{current_dir}/{filename}")

    def test_repodata_and_get_index(self):
        repodata = utils.repodata()
        indexes = utils.get_index(repodata)
        assert set(["clusters", "networks"]).issubset(indexes)

    def fake_mkdir(self, dir):
        pass

    def test_initdir(self, monkeypatch):
        monkeypatch.setattr(neo.libs.utils, "mkdir", self.fake_mkdir)
        assert ["instances"] == utils.initdir(manifest.fake_manifest)

    def fake_template_git(self, url, dir_, branch):
        return url, dir_, branch

    def test_template_url_local(self, monkeypatch):
        monkeypatch.setattr(neo.libs.utils, "template_git", self.fake_template_git)
        url = "local+https://github.com/BiznetGIO/neo-heat-kubernetes.git"
        dest = "path/to/deploy/dir"
        branch = "0.1.17"
        assert (
            utils.template_url(url, dest, branch)
            == "https://github.com/BiznetGIO/neo-heat-kubernetes.git"
        )

    def test_template_url_git(self, monkeypatch):
        monkeypatch.setattr(neo.libs.utils, "template_git", self.fake_template_git)
        url = "git+https://github.com/BiznetGIO/neo-heat-kubernetes.git"
        dest = "path/to/deploy/dir"
        branch = "0.1.17"
        assert utils.template_url(url, dest, branch) == (
            "https://github.com/BiznetGIO/neo-heat-kubernetes.git",
            "path/to/deploy/dir",
            "0.1.17",
        )

    def test_get_project(self):
        current_path = path.abspath(path.dirname(__file__))
        parent_path = pathlib.Path(current_path).parent
        assert ["awesome-project"] == utils.get_project(
            f"{parent_path}/fixtures/manifest.yml"
        )

    def test_do_deploy_dir(self):
        current_path = path.abspath(path.dirname(__file__))
        parent_path = pathlib.Path(current_path).parent
        manifest_path = f"{parent_path}/fixtures/manifest.yml"
        deploy_path = f"{parent_path}/fixtures/.deploy/"

        utils.do_deploy_dir(manifest_path)
        is_exist = path.isdir(deploy_path)
        os.rmdir(deploy_path)

        assert is_exist is True
