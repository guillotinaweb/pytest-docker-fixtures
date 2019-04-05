from ._base import BaseImage
from time import sleep


class Redis(BaseImage):
    label = 'redis'
    name = 'redis'
    port = 6379

    def check(self):
        sleep(1)
        return True


redis_image = Redis()
