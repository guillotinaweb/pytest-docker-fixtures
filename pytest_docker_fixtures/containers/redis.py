from ._base import BaseImage
from time import sleep


class Redis(BaseImage):
    label = 'redis'
    name = 'redis'
    port = 6379

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(dict(
            cap_add=['IPC_LOCK'],
            mem_limit='200m'
        ))
        return image_options

    def check(self):
        sleep(1)
        return True


redis_image = Redis()
