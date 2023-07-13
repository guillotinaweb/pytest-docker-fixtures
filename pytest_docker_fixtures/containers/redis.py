from .base import BaseContainer
from .base import ContainerConfiguration
from time import sleep


class Redis(BaseContainer):
    name: str = "redis"
    config: ContainerConfiguration = ContainerConfiguration(
        image="redis",
        version="7.0.10",
        port=6379,
        options={"cap_add": ["IPC_LOCK"], "mem_limit": "200m"},
    )

    def check(self):
        sleep(1)
        return True


redis_container = Redis()
