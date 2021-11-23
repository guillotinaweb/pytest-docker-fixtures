from ._base import BaseImage


class Memcached(BaseImage):
    label = 'memcached'
    name = 'memcached'
    port = 11211

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


memcached_image = Memcached()
