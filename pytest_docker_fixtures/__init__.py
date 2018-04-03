from .containers.cockroach import cockroach_image
from .containers.es import es_image
from .containers.etcd import etcd_image
from .containers.pg import pg_image
from .containers.redis import redis_image

import os
import pytest


IS_TRAVIS = 'TRAVIS' in os.environ


@pytest.fixture(scope='session')
def redis():
    """
    detect travis, use travis's postgres; otherwise, use docker
    """
    if 'TRAVIS' in os.environ:
        host = 'localhost'
        port = 6379
    else:
        host, port = redis_image.run()

    yield host, port  # provide the fixture value

    if 'TRAVIS' not in os.environ:
        redis_image.stop()


@pytest.fixture(scope='session')
def cockroach():
    yield cockroach_image.run()
    cockroach_image.stop()


@pytest.fixture(scope='session')
def pg():
    if 'TRAVIS' in os.environ:
        host = 'localhost'
        port = 6379
    else:
        host, port = pg_image.run()

    yield host, port  # provide the fixture value

    if 'TRAVIS' not in os.environ:
        pg_image.stop()


@pytest.fixture(scope='session')
def etcd():
    yield etcd_image.run()
    etcd_image.stop()


@pytest.fixture(scope='session')
def es():
    yield es_image.run()
    es_image.stop()
