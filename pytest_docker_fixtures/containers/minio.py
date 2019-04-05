from ._base import BaseImage

import requests


class Minio(BaseImage):
    name = 'minio'
    port = 9000

    def check(self):
        url = f'http://{self.host}:{self.get_port()}/'
        try:
            resp = requests.options(url)
            if 200 <= resp.status_code < 500:
                return True
        except Exception:
            pass
        return False


minio_image = Minio()
