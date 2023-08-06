import pytest

import neo.libs.vm
from neo.libs import vm


class TestVm:
    @pytest.fixture
    def fake_nova_client(session, mocker, monkeypatch):
        def fake_get_console_logs(*args, **kwargs):
            logs = "fake logs"
            if "length" in kwargs:
                logs = "fake logs", kwargs["length"]
            return logs

        def fake_compute(session):
            fake_compute = mocker.Mock()
            fake_compute.servers.list.return_value = ["fake_server1", "fake_server2"]
            fake_compute.servers.get.return_value = "fake_server_info"
            fake_compute.flavors.list.return_value = ["fake_flavor1", "fake_flavor2"]
            fake_compute.flavors.get.return_value = "fake_flavor_info"
            fake_compute.keypairs.list.return_value = ["fake_key1", "fake_key2"]
            fake_compute.servers.get_console_output = fake_get_console_logs
            return fake_compute

        monkeypatch.setattr(neo.libs.vm, "get_nova_client", fake_compute)

    def test_get_list(self, fake_nova_client):
        assert vm.get_list(session="fake_session") == ["fake_server1", "fake_server2"]

    def test_detail(self, fake_nova_client):
        assert vm.detail("123") == "fake_server_info"

    def test_get_flavor(self, fake_nova_client):
        assert vm.get_flavor(session="fake_session") == ["fake_flavor1", "fake_flavor2"]

    def test_detail_flavor(self, fake_nova_client):
        assert vm.detail_flavor("123", session="fake_session") == "fake_flavor_info"

    def test_get_keypairs(self, fake_nova_client):
        assert vm.get_keypairs(session="fake_session") == ["fake_key1", "fake_key2"]

    def test_get_console_log(self, fake_nova_client):
        assert vm.get_console_logs("123") == "fake logs"
        assert vm.get_console_logs("123", length=10) == ("fake logs", 10)
