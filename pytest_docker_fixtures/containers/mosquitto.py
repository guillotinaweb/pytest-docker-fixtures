from .base import BaseImage, ContainerConfiguration


class Mosquitto(BaseImage):
    name: str = "mosquitto"
    config: ContainerConfiguration = ContainerConfiguration(
        image="eclipse-mosquitto",
        version="2.0.15",
        options={
            "command": "mosquitto -c /mosquitto-no-auth.conf",
            "publish_all_ports": False,
            "ports": {"1883/tcp": None},
        },
    )

    def check(self) -> bool:
        """Check if container is started."""
        return f"mosquitto version {self.config.version} running" in self.logs()


mosquitto_image = Mosquitto()
