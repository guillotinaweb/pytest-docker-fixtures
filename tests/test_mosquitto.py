from pytest_docker_fixtures.containers.base import HostPort
from pytest_docker_fixtures.containers.mosquitto import mosquitto_container
from tests.util import verify_started


CUSTOM_PORT = 1883
mosquitto_container.config.options.update(
    {
        "ports": {"1883/tcp": CUSTOM_PORT},
    }
)


def test_started(mosquitto: HostPort) -> None:
    verify_started(mosquitto, mosquitto_container)


def test_custom_port(mosquitto: HostPort) -> None:
    assert mosquitto.port == CUSTOM_PORT
