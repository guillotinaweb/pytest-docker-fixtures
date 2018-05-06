from ._base import BaseImage

import os
import requests


class ElasticSearch(BaseImage):
    name = 'elasticsearch'
    port = 9200

    def get_image_options(self):
        image_options = super().get_image_options()
        env = {
            'cluster.name': 'docker-cluster',
            'ES_JAVA_OPTS': '-Xms512m -Xmx512m',
            "xpack.security.enabled": "false",
            #"http.host=0.0.0.0" -e "transport.host=127.0.0.1"
        }
        if 'oss' in self.image:
            del env['xpack.security.enabled']
        image_options.update(dict(
            cap_add=['IPC_LOCK'],
            mem_limit='1g',
            environment=env
        ))
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
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return True
        except:
            pass
        return False


es_image = ElasticSearch()
