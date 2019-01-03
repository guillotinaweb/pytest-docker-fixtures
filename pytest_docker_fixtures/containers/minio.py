from ._base import BaseImage
from time import sleep


class Minio(BaseImage):
    name = 'minio'

    @property
    def image(self):
        return 'minio/minio'

    def get_image_options(self):
        image_options = super().get_image_options()

        image_options.update(dict(
            cap_add=['IPC_LOCK'],
            mem_limit='200m',
            command='server /export',
            environment={
                'MINIO_ACCESS_KEY': 'x' * 10,
                'MINIO_SECRET_KEY': 'x' * 10,
            },
            publish_all_ports=False,
            ports={
                '9000/tcp': '19000'
            }
        ))
        return image_options

    def check(self):
        sleep(1)
        return True


minio_image = Minio()
