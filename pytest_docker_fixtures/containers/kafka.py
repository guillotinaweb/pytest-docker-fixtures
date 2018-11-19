from ._base import BaseImage


class Kafka(BaseImage):
    label = 'kafka'
    name = 'kafka'
    port = 9092

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(dict(
            environment={
                'ADVERTISED_PORT': '9092',
                'ADVERTISED_HOST': '0.0.0.0'
            },
            ports={
                f'9092': '9092',
                f'2181': '2181'
            }
        ))
        return image_options

    def check(self):
        try:
            from kafka import KafkaClient
            from kafka.common import KafkaUnavailableError
            KafkaClient(f"{self.host}:{self.get_port()}")
            return True
        except KafkaUnavailableError:
            pass
        return False


kafka_image = Kafka()
