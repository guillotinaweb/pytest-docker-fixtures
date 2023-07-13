from .base import BaseContainer
from .base import ContainerConfiguration


class Memcached(BaseContainer):
    name: str = "memcached"
    config: ContainerConfiguration = ContainerConfiguration(
        image="memcached", version="1.6.7", port=11211
    )

    def check(self):
        local_port = self.get_port()

        from pymemcache.client.base import Client

        client = Client((self.host, local_port))
        try:
            server_stats = client.stats()
            return server_stats[b"accepting_conns"] == 1
        except (ConnectionRefusedError, KeyError):
            # not ready yet
            return False


memcached_container = Memcached()
