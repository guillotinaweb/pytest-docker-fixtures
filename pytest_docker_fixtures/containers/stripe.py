import requests

from ._base import BaseImage


class Stripe(BaseImage):
    label = "stripe"
    name = "stripe"
    port = 12111                # HTTP port

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
