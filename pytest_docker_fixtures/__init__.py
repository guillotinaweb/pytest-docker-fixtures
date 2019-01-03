from .containers.cockroach import cockroach_image
from .containers.es import es_image
from .containers.etcd import etcd_image
from .containers.pg import pg_image
from .containers.redis import redis_image
from .containers.rabbitmq import rabbitmq_image
from .containers.kafka import kafka_image
from .containers.minio import minio_image

import os
import pytest


IS_TRAVIS = 'TRAVIS' in os.environ


@pytest.fixture(scope='session')
def redis():
    """
    detect travis, use travis's postgres; otherwise, use docker
    """
    if IS_TRAVIS:
        host = 'localhost'
        port = 6379
    else:
        host, port = redis_image.run()

    yield host, port  # provide the fixture value

    if not IS_TRAVIS:
        redis_image.stop()


@pytest.fixture(scope='session')
def cockroach():
    yield cockroach_image.run()
    cockroach_image.stop()


@pytest.fixture(scope='session')
def pg():
    if IS_TRAVIS:
        host = 'localhost'
        port = 6379
    else:
        host, port = pg_image.run()

    yield host, port  # provide the fixture value

    if not IS_TRAVIS:
        pg_image.stop()


@pytest.fixture(scope='session')
def etcd():
    yield etcd_image.run()
    etcd_image.stop()


@pytest.fixture(scope='session')
def es():
    yield es_image.run()
    es_image.stop()


@pytest.fixture(scope='session')
def rabbitmq():
    yield rabbitmq_image.run()
    rabbitmq_image.stop()


@pytest.fixture(scope='session')
def kafka():
    yield kafka_image.run()
    kafka_image.stop()


@pytest.fixture(scope='session')
def minio():
    if IS_TRAVIS:
        host = 'localhost'
        port = 19000
    else:
        host, port = minio_image.run()

    yield host, port

    if not IS_TRAVIS:
        minio_image.stop()
