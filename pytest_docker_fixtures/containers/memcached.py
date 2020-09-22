from ._base import BaseImage
from time import sleep


class Memcached(BaseImage):
    label = 'memcached'
    name = 'memcached'
    port = 11211

    def check(self):
        sleep(1)
        return True


memcached_image = Memcached()
