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
            resp = requests.get(
                f'{url}_cluster/health',
                params={
                    'wait_for_status': 'yellow',
                    'timeout': '1s'
                },
                timeout=3)
            if (resp.status_code == 200 and
                    resp.json().get('status') in ('yellow', 'green')):
                return True
        except Exception:
            try:
                # work with ssl
                resp = requests.get(
                    f'{ssl_url}_cluster/health',
                    auth=('admin', 'admin'),
                    params={
                        'wait_for_status': 'yellow',
                        'timeout': '1s'
                    },
                    timeout=3,
                    verify=False)
                if (resp.status_code == 200 and
                        resp.json().get('status') in ('yellow', 'green')):
                    return True
            except Exception:
                pass
        return False


es_image = ElasticSearch()
