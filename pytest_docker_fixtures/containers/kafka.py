from ._base import BaseImage


class Kafka(BaseImage):
    label = 'kafka'
    name = 'kafka'
    port = 9092

    def check(self):
        from kafka import KafkaClient
        from kafka.common import KafkaUnavailableError
        try:
            KafkaClient(f"{self.host}:{self.get_port()}")
            return True
        except KafkaUnavailableError:
            pass
        return False


kafka_image = Kafka()
