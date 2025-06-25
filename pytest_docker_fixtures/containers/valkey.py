from ._base import BaseImage
from time import sleep


class Valkey(BaseImage):
    label = 'valkey'
    name = 'valkey'
    port = 6379

    def check(self):
        sleep(1)
        return True


valkey_image = Valkey()
