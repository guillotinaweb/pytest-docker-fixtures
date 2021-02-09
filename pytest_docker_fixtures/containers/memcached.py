from ._base import BaseImage


class Memcached(BaseImage):
    label = 'memcached'
    name = 'memcached'
    port = 11211

    def check(self):
        local_port = self.get_port()

        from pymemcache.client.base import Client
        client = Client(("localhost", local_port))
        server_stats = None
        try:
            server_stats = client.stats()
            print("EEEEEEEP")
            print(server_stats)
            return server_stats[b"accepting_conns"] == 1
        except (ConnectionRefusedError, KeyError) as ex:
            raise Exception(server_stats) from ex
            # not ready yet
            return False


memcached_image = Memcached()
