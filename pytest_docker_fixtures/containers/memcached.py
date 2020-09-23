from ._base import BaseImage
from pymemcache.client.base import Client


class Memcached(BaseImage):
    label = 'memcached'
    name = 'memcached'
    port = 11211

    def check(self):
        local_port = self.get_port()
        client = Client(("localhost", local_port))
        try:
            server_stats = client.stats()
            return server_stats[b"accepting_conns"] == 1
        except (ConnectionRefusedError, KeyError):
            # not ready yet
            return False


memcached_image = Memcached()
