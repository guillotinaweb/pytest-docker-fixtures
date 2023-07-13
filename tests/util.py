from pytest_docker_fixtures.containers.base import BaseContainer


def verify_started(service: tuple[str, int], image: BaseContainer) -> None:
    assert image.container.status == "running"
    assert service[0] == image.host
    assert service[1] == image.get_port()
