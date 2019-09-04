from .containers.cockroach import cockroach_image
from .containers.es import es_image
from .containers.etcd import etcd_image
from .containers.pg import pg_image
from .containers.redis import redis_image
from .containers.rabbitmq import rabbitmq_image
from .containers.kafka import kafka_image
from .containers.minio import minio_image
from .containers.mysql import mysql_image

import os
import pytest


IS_TRAVIS = 'TRAVIS' in os.environ


@pytest.fixture(scope='session')
def redis():
    """
    detect travis, use travis's postgres; otherwise, use docker
    """
    if os.environ.get('REDIS'):
        yield os.environ['REDIS'].split(':')
    else:
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
    if os.environ.get('COCKROACH'):
        yield os.environ['COCKROACH'].split(':')
    else:
        yield cockroach_image.run()
        cockroach_image.stop()


@pytest.fixture(scope='session')
def pg():
    if os.environ.get('POSTGRESQL'):
        yield os.environ['POSTGRESQL'].split(':')
    else:
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
    if os.environ.get('ETCD'):
        yield os.environ['ETCD'].split(':')
    else:
        yield etcd_image.run()
        etcd_image.stop()


@pytest.fixture(scope='session')
def es():
    if os.environ.get('ELASTICSEARCH'):
        yield os.environ['ELASTICSEARCH'].split(':')
    else:
        yield es_image.run()
        es_image.stop()


@pytest.fixture(scope='session')
def rabbitmq():
    if os.environ.get('RABBITMQ'):
        yield os.environ['RABBITMQ'].split(':')
    else:
        yield rabbitmq_image.run()
        rabbitmq_image.stop()


@pytest.fixture(scope='session')
def kafka():
    if os.environ.get('KAFKA'):
        yield os.environ['KAFKA'].split(':')
    else:
        yield kafka_image.run()
        kafka_image.stop()


@pytest.fixture(scope='session')
def minio():
    if os.environ.get('MINIO'):
        yield os.environ['MINIO'].split(':')
    else:
        if IS_TRAVIS:
            host = 'localhost'
            port = 19000
        else:
            host, port = minio_image.run()

        yield host, port

        if not IS_TRAVIS:
            minio_image.stop()


@pytest.fixture(scope='session')
def mysql():
    if os.environ.get('MYSQL'):
        yield os.environ['MYSQL'].split(':')
    else:
        yield mysql_image.run()
        mysql_image.stop()
