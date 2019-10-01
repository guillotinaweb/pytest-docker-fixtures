settings = {
    'cockroach': {
        'image': 'cockroachdb/cockroach',
        'version': 'v1.1.7',
        'options': {
            'command': ' '.join([
                'start --insecure',
            ]),
            'publish_all_ports': False,
            'ports': {
                f'26257/tcp': '26257'
            }
        }
    },
    'elasticsearch': {
        'image': 'elasticsearch',
        'version': '5.2.0',
        'env': {
            'cluster.name': 'docker-cluster',
            'ES_JAVA_OPTS': '-Xms512m -Xmx512m',
            "xpack.security.enabled": "false"
        },
        'options': {
            'cap_add': ['IPC_LOCK'],
            'mem_limit': '1g'
        }
    },
    'etcd': {
        'image': 'quay.io/coreos/etcd',
        'version': 'v3.2.0-rc.0'
    },
    'minio': {
        'image': 'minio/minio',
        'version': 'latest',
        'env': {
            'MINIO_ACCESS_KEY': 'x' * 10,
            'MINIO_SECRET_KEY': 'x' * 10,
        },
        'options': {
            'cap_add': ['IPC_LOCK'],
            'mem_limit': '200m',
            'command': 'server /export',
        }
    },
    'mysql': {
        'image': 'mysql',
        'version': '5.7',
        'env': {
            'MYSQL_ALLOW_EMPTY_PASSWORD': 'yes'
        }
    },
    'postgresql': {
        'image': 'postgres',
        'version': '9.6',
        'env': {
            'POSTGRES_PASSWORD': '',
            'POSTGRES_DB': 'guillotina',
            'POSTGRES_USER': 'postgres'
        }
    },
    'redis': {
        'image': 'redis',
        'version': '3.2.8',
        'options': {
            'cap_add': ['IPC_LOCK'],
            'mem_limit': '200m'
        }
    },
    'rabbitmq': {
        'image': 'rabbitmq',
        'version': '3.7.8'
    },
    'kafka': {
        'image': 'spotify/kafka',
        'version': 'latest',
        'env': {
            'ADVERTISED_PORT': '9092',
            'ADVERTISED_HOST': '0.0.0.0'
        },
        'options': {
            'ports': {
                '9092': '9092',
                '2181': '2181'
            }
        }
    }
}


def get_image(name):
    image = settings[name]
    return image['image'] + ':' + image['version']


def configure(name, image=None, version=None, full=None,
              env=None, options=None, max_wait_s=None):
    if full is not None:
        image, _, version = full.partition(':')
    if image is not None:
        settings[name]['image'] = image
    if version is not None:
        settings[name]['version'] = version
    if env is not None:
        if 'env' not in settings[name]:
            settings[name]['env'] = {}
        settings[name]['env'].update(env)
    if max_wait_s:
        settings[name]['max_wait_s'] = max_wait_s


def get_env(name):
    image = settings[name]
    return image.get('env') or {}

def get_max_wait_s(name):
    # Default to 30 seconds
    image = settings[name]
    return image.get('max_wait_s') or 30

def get_options(name):
    image = settings[name]
    return image.get('options') or {}
