from pytest_docker_fixtures.containers.etcd import etcd_container
from tests.util import verify_started


def test_started(etcd) -> None:
    verify_started(etcd, etcd_container)
