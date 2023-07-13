from .base import BaseContainer
from .base import ContainerConfiguration

import random


image_name = f"test-etcd-{random.randint(0, 1000)}"


class ETCD(BaseContainer):
    name: str = "etcd"
    config: ContainerConfiguration = ContainerConfiguration(
        image="quay.io/coreos/etcd", version="v3.2.0-rc.0", port=2379
    )

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(
            {
                "mem_limit": "200m",
                "name": image_name,
                "command": " ".join(
                    [
                        "/usr/local/bin/etcd",
                        f"--name {image_name}",
                        "--data-dir /etcd-data",
                        "--listen-client-urls http://0.0.0.0:2379",
                        "--advertise-client-urls http://0.0.0.0:2379",
                        "--listen-peer-urls http://0.0.0.0:2380",
                        "--initial-advertise-peer-urls http://0.0.0.0:2380",
                        f"--initial-cluster {image_name}=http://0.0.0.0:2380",
                        "--initial-cluster-token my-etcd-token",
                        "--initial-cluster-state new",
                        "--auto-compaction-retention 1",
                    ]
                ),
            }
        )
        return image_options

    def check(self) -> bool:
        return True


etcd_container = ETCD()
