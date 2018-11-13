from ._base import BaseImage
from time import sleep


class Kafka(BaseImage):
    label = 'kafka'
    name = 'kafka'
    port = 9092

    def get_image_options(self):
        image_options = super().get_image_options()
        # image_options.update(dict(
        #     cap_add=['IPC_LOCK'],
        #     mem_limit='200m'
        # ))
        return image_options

    def check(self):
        sleep(1)
        return True


kafka_image = Kafka()
