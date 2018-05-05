settings = {
    'cockroach': {
        'image': 'cockroachdb/cockroach',
        'version': 'v1.1.7'
    },
    'elasticsearch': {
        'image': 'elasticsearch',
        'version': '5.2.0'
    },
    'etcd': {
        'image': 'quay.io/coreos/etcd',
        'version': 'v3.2.0-rc.0'
    },
    'postgresql': {
        'image': 'postgres',
        'version': '9.6'
    },
    'redis': {
        'image': 'redis',
        'version': '3.2.8'
    }
}

def get_image(name):
    image = settings[name]
    return image['image'] + ':' + image['version']

def configure(name, image=None, version=None, full=None):
    if full is not None:
        image, _, version = full.partition(':')
    if image is not None:
        settings[name]['image'] = image
    if version is not None:
        settings[name]['version'] = version