from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass, field
from datetime import datetime
from pprint import pformat
from time import sleep
from typing import Any, NamedTuple, Optional, Union

import docker
import os
import re

from docker.models.containers import Container
from docker.errors import APIError, NotFound
from docker.client import DockerClient

DOCKER_HOST_TCP_FORMAT = re.compile(r"^tcp://(\d+\.\d+\.\d+\.\d+)(?::\d+)?$")


class ContainerNotStartedException(Exception):
    pass


@dataclass()
class ContainerConfiguration:
    image: str
    version: str = "latest"
    port: Union[None, int] = None
    env: dict[str, Any] = field(default_factory=lambda: {})
    options: dict[str, Any] = field(default_factory=lambda: {})
    max_wait_started: int = 30


HostPort = namedtuple("HostPort", ["host", "port"])


class BaseImage(ABC):
    docker_version = "auto"
    base_image_options: dict[str, Any] = {
        "cap_add": ["IPC_LOCK"],
        "mem_limit": "1g",
        "environment": {},
        "detach": True,
        "publish_all_ports": True,
    }

    @property
    @abstractmethod
    def name(self) -> str:
        """Container name."""

    @property
    @abstractmethod
    def config(self) -> ContainerConfiguration:
        """Container configuration."""

    @abstractmethod
    def check(self):
        """Checks if container is started successfully."""

    def __init__(self) -> None:
        self.container: Optional[Container] = None
        self._start_time: datetime = datetime(1, 1, 1)

    @property
    def image(self) -> str:
        return f"{self.config.image}:{self.config.version}"

    @property
    def host(self) -> str:
        return self.get_host()

    def get_ports(self) -> dict[str, int]:
        if self.container is None:
            raise ContainerNotStartedException

        network = self.container.attrs["NetworkSettings"]
        result = {}
        for port, value in network["Ports"].items():
            if port == "6543/tcp":
                continue

            result[port] = int(value[0]["HostPort"])

        return result

    def get_port(self, port: Union[None, str, int] = None) -> int:
        if port is None:
            port = self.config.port
        if port is None:
            port = next(iter(self.config.options["ports"]))
        if isinstance(port, int):
            port = f"{port}/tcp"

        assert isinstance(port, str)

        return self.get_ports()[port]

    def get_host(self) -> str:
        if self.container is None:
            raise ContainerNotStartedException

        host = self.container.attrs["NetworkSettings"]["IPAddress"]

        if host != "":
            if os.environ.get("TESTING", "") == "jenkins":
                pass

            # Support remote docker instance exposed via tcp
            # https://docs.docker.com/engine/reference/commandline/cli/
            elif DOCKER_HOST_TCP_FORMAT.match(os.environ.get("DOCKER_HOST", "")):
                remote_docker_host_ip = DOCKER_HOST_TCP_FORMAT.match(
                    os.environ.get("DOCKER_HOST", "")
                ).group(1)
                host = remote_docker_host_ip
            else:
                host = "localhost"

        return host

    def get_image_options(self) -> dict[str, Any]:
        image_options = self.base_image_options.copy()
        env: dict[str, Any] = image_options.setdefault("environment", {})

        for key, value in self.config.env.items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value

        image_options.update(self.config.options)
        return image_options

    def logs(self, since_last_start: bool = True) -> str:
        """Get docker container logs."""
        if self.container is None:
            raise ContainerNotStartedException

        if since_last_start:
            logs: bytes = self.container.logs(since=self._start_time)
        else:
            logs = self.container.logs()
        return logs.decode("utf-8")

    def run(self) -> HostPort:
        docker_client: DockerClient = docker.from_env(version=self.docker_version)
        image_options = self.get_image_options()

        # Create a new one
        self.container = docker_client.containers.run(image=self.image, **image_options)
        container_id = self.container.id
        count = 0

        self.container = docker_client.containers.get(container_id)

        started = False

        print(f"starting {self.name}")
        while count < self.config.max_wait_started and not started:
            if count > 0:
                sleep(1)
            count += 1

            try:
                self.container = docker_client.containers.get(container_id)
            except NotFound:
                print(f"Container not found for {self.name}")
                continue

            if self.container.status == "exited":
                logs = self.container.logs()
                self.stop()
                raise Exception(f"Container failed to start {logs}")

            if self.get_host() != "":
                started = self.check()

        if not started:
            logs = self.container.logs().decode("utf-8")
            self.stop()
            raise Exception(
                f"Could not start {self.name}: {logs}\n"
                f"Image: {self.image}\n"
                f"Options:\n{pformat(image_options)}"
            )

        print(f"{self.name} started")
        self._start_time = datetime.now()

        return HostPort(self.get_host(), self.get_port())

    def stop(self) -> None:
        if self.container is not None:
            try:
                self.container.kill()
            except APIError:
                pass
            try:
                self.container.remove(v=True, force=True)
            except APIError:
                pass
