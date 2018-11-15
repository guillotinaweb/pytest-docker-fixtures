from ._base import BaseImage


class RabbitMQ(BaseImage):
    label = 'rabbitmq'
    name = 'rabbitmq'
    port = 5672

    def get_image_options(self):
        image_options = super().get_image_options()
        return image_options

    def check(self):
        import pika
        from pika.connection import URLParameters
        url = f'amqp://guest:guest@{self.host}:{self.get_port()}/%2F'
        try:
            connection = pika.BlockingConnection(URLParameters(url))
        except Exception:
            return False
        else:
            return connection.is_open


rabbitmq_image = RabbitMQ()
