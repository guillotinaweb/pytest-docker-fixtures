from .base import BaseContainer
from .base import ContainerConfiguration

import requests


class Minio(BaseContainer):
    name: str = "minio"
    config: ContainerConfiguration = ContainerConfiguration(
        image="minio/minio",
        port=9000,
        env={
            "MINIO_ACCESS_KEY": "x" * 10,
            "MINIO_SECRET_KEY": "x" * 10,
        },
        options={
            "cap_add": ["IPC_LOCK"],
            "mem_limit": "200m",
            "command": "server /export",
        },
    )

    def check(self):
        url = f"http://{self.host}:{self.get_port()}/"
        try:
            resp = requests.options(url)
            if 200 <= resp.status_code < 500:
                return True
        except Exception:
            pass
        return False


minio_container = Minio()
