from ._base import BaseImage
from time import sleep


class Kafka(BaseImage):
    label = 'kafka'
    name = 'kafka'
    port = 9092

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(dict(
            environment={
                'ADVERTISED_PORT': '9092',
                'ADVERTISED_HOST': 'localhost'
            },
            ports={
                f'9092': '9092',
                f'2181': '2181'
            }
        ))
        return image_options

    def check(self):
        sleep(1)
        return True


kafka_image = Kafka()
