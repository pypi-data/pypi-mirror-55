import mock

import neo.libs.vm
import neo.libs.image
import neo.libs.network
from neo.libs import lambdafunc


class TestLambdafunc:
    def test_get_flavor_file_exists(self, fs):
        flavor_contents = """ data:
        - SX48.8
        - SX48.12
        """
        flavor_file = "/tmp/.flavor.yml"
        fs.create_file(flavor_file, contents=flavor_contents)
        assert lambdafunc.get_flavor() == ["SX48.8", "SX48.12"]

    def fake_get_flavor(self, session=None):
        flavor_1 = mock.Mock()
        flavor_2 = mock.Mock()
        flavor_1.name = "SS2.1"
        flavor_2.name = "SL24.8"
        return [flavor_1, flavor_2]

    def test_get_flavor_no_file(self, monkeypatch):
        monkeypatch.setattr(neo.libs.vm, "get_flavor", self.fake_get_flavor)
        assert lambdafunc.get_flavor() == ["SS2.1", "SL24.8"]

    # img

    def test_get_img_file_exists(self, fs):
        img_contents = """ data:
        - CentOS 6.9
        - Debian 9
        """
        img_file = "/tmp/.images.yml"
        fs.create_file(img_file, contents=img_contents)
        assert lambdafunc.get_img() == ["CentOS 6.9", "Debian 9"]

    def fake_get_img_list(self, session=None):
        img_1 = mock.Mock()
        img_2 = mock.Mock()
        img_1.name = "Fedora 25"
        img_2.name = "Fedora 26"
        return [img_1, img_2]

    def test_get_img_no_file(self, monkeypatch):
        monkeypatch.setattr(neo.libs.image, "get_list", self.fake_get_img_list)
        assert lambdafunc.get_img() == ["Fedora 26", "Fedora 25"]

    # key

    def fake_get_keypairs(self, session=None):
        key_1 = mock.Mock()
        key_2 = mock.Mock()
        key_1.name = "ssm"
        key_2.name = "vm-key"
        return [key_1, key_2]

    def test_get_key(self, monkeypatch):
        monkeypatch.setattr(neo.libs.vm, "get_keypairs", self.fake_get_keypairs)
        assert lambdafunc.get_key() == ["ssm", "vm-key"]

    # net

    def fake_get_network_list(self, session=None):
        net_1 = {"name": "ssm-net"}
        net_2 = {"name": "vm-net"}
        return [net_1, net_2]

    def test_get_network_list(self, monkeypatch):
        monkeypatch.setattr(neo.libs.network, "get_list", self.fake_get_network_list)
        assert lambdafunc.get_network() == ["ssm-net", "vm-net"]
