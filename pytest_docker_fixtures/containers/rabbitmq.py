from .base import BaseContainer
from .base import ContainerConfiguration


class RabbitMQ(BaseContainer):
    name: str = "rabbitmq"
    config: ContainerConfiguration = ContainerConfiguration(
        image="rabbitmq", version="3.7.8", port=5672
    )

    def check(self):
        from pika.connection import URLParameters

        import pika

        url = f"amqp://guest:guest@{self.host}:{self.get_port()}/%2F"
        try:
            connection = pika.BlockingConnection(URLParameters(url))
        except Exception:
            return False
        else:
            return connection.is_open


rabbitmq_container = RabbitMQ()
