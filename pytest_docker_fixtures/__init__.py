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
    try:
        if IS_TRAVIS:
            host = 'localhost'
            port = 6379
        else:
            host, port = redis_image.run()

        yield host, port  # provide the fixture value
    finally:
        if not IS_TRAVIS:
            redis_image.stop()


@pytest.fixture(scope='session')
def cockroach():
    try:
        yield cockroach_image.run()
    finally:
        cockroach_image.stop()


@pytest.fixture(scope='session')
def pg():
    try:
        if IS_TRAVIS:
            host = 'localhost'
            port = 6379
        else:
            host, port = pg_image.run()

        yield host, port  # provide the fixture value
    finally:
        if not IS_TRAVIS:
            pg_image.stop()


@pytest.fixture(scope='session')
def etcd():
    try:
        yield etcd_image.run()
    finally:
        etcd_image.stop()


@pytest.fixture(scope='session')
def es():
    try:
        yield es_image.run()
    finally:
        es_image.stop()


@pytest.fixture(scope='session')
def rabbitmq():
    try:
        yield rabbitmq_image.run()
    finally:
        rabbitmq_image.stop()


@pytest.fixture(scope='session')
def kafka():
    try:
        yield kafka_image.run()
    finally:
        kafka_image.stop()


@pytest.fixture(scope='session')
def minio():
    try:
        if IS_TRAVIS:
            host = 'localhost'
            port = 6379
        else:
            host, port = minio_image.run()

        yield host, port
    finally:
        if not IS_TRAVIS:
            minio_image.stop()
