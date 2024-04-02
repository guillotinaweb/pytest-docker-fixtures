from ._base import BaseImage

import requests


class EMQX(BaseImage):
    name = 'emqx'
    port = 1883

    def check(self):
        port = self.get_port(18083)
        url = f"http://{self.host}:{port}/status"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return True
        except Exception:
            return False


emqx_image = EMQX()
