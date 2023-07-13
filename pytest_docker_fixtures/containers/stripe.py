from .base import BaseImage
from .base import ContainerConfiguration

import requests


class Stripe(BaseImage):
    name: str = "stripe"
    config: ContainerConfiguration = ContainerConfiguration(
        image="stripe/stripe-mock",
        version="v0.136.0",
        options={
            "ports": {
                "12111": "12111",  # HTTP (default)
                "12112": "12112",  # HTTPS
            }
        },
    )

    def check(self):
        url = f"http://{self.host}:{self.get_port()}/"
        try:
            resp = requests.get(url)
            if 200 <= resp.status_code < 500:
                return True
        except Exception:
            pass

        return False


stripe_image = Stripe()
