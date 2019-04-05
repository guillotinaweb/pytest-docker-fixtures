from ._base import BaseImage

import os
import requests


class ElasticSearch(BaseImage):
    name = 'elasticsearch'
    port = 9200

    def get_image_options(self):
        image_options = super().get_image_options()
        if 'TRAVIS' in os.environ:
            image_options.update({
                'publish_all_ports': False,
                'ports': {
                    f'9200/tcp': '9200'
                }
            })
        return image_options

    def check(self):
        url = f'http://{self.host}:{self.get_port()}/'
        ssl_url = url.replace('http://', 'https://')
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return True
        except Exception:
            try:
                # work with ssl
                resp = requests.get(
                    ssl_url, auth=('admin', 'admin'), verify=False)
                if resp.status_code == 200:
                    return True
            except Exception:
                pass
        return False


es_image = ElasticSearch()
