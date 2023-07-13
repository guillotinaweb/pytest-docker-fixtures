from .base import BaseImage
from .base import ContainerConfiguration


class Kafka(BaseImage):
    name = "kafka"
    config: ContainerConfiguration = ContainerConfiguration(
        image="spotify/kafka",
        port=9092,
        env={"ADVERTISED_PORT": "9092", "ADVERTISED_HOST": "0.0.0.0"},
        options={"ports": {"9092": "9092", "2181": "2181"}},
    )

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
