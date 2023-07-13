from pytest_docker_fixtures.containers.base import BaseImage, HostPort


def verify_started(service: tuple[str, int], image: BaseImage) -> None:
    assert image.container.status == "running"
    assert service[0] == image.host
    assert service[1] == image.get_port()
