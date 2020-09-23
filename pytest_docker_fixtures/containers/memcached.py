from ._base import BaseImage
from memcache import Client


class Memcached(BaseImage):
    label = 'memcached'
    name = 'memcached'
    port = 11211

    def check(self):
        local_port = self.get_port()
        servers = [f"localhost:{local_port}"]
        client = Client(servers, debug=1)
        server_stats = client.get_stats()
        try:
            return server_stats[0][1]["accepting_conns"] == "1"
        except (IndexError, KeyError):
            # not ready yet
            return False


memcached_image = Memcached()
