from ._base import BaseImage

import os
import requests


ELASTICSEACH_IMAGE = 'elasticsearch:5.2.0'


class ElasticSearch(BaseImage):
    name = 'elasticsearch'
    image = ELASTICSEACH_IMAGE
    port = 9200

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(dict(
            cap_add=['IPC_LOCK'],
            mem_limit='1g',
            environment={
                'cluster.name': 'docker-cluster',
                'bootstrap.memory_lock': True,
                'ES_JAVA_OPTS': '-Xms512m -Xmx512m'
            }
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
