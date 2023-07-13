from .containers.cockroach import cockroach_container
from .containers.es import es_container
from .containers.etcd import etcd_container
from .containers.kafka import kafka_container
from .containers.memcached import memcached_container
from .containers.minio import minio_container
from .containers.mosquitto import mosquitto_container
from .containers.mysql import mysql_container
from .containers.pg import pg_container
from .containers.rabbitmq import rabbitmq_container
from .containers.redis import redis_container
from .containers.stripe import stripe_container
from pytest_docker_fixtures.containers.base import HostPort
from typing import Generator

import os
import pytest


IS_TRAVIS = "TRAVIS" in os.environ


@pytest.fixture(scope="session")
def redis():
    """
    detect travis, use travis's postgres; otherwise, use docker
    """
    if os.environ.get("REDIS"):
        yield os.environ["REDIS"].split(":")
    else:
        if IS_TRAVIS:
            host = "localhost"
            port = 6379
        else:
            host, port = redis_container.run()

        yield host, port  # provide the fixture value

        if not IS_TRAVIS:
            redis_container.stop()


@pytest.fixture(scope="session")
def cockroach():
    if os.environ.get("COCKROACH"):
        yield os.environ["COCKROACH"].split(":")
    else:
        yield cockroach_container.run()
        cockroach_container.stop()


@pytest.fixture(scope="session")
def pg():
    if os.environ.get("POSTGRESQL"):
        yield os.environ["POSTGRESQL"].split(":")
    else:
        if IS_TRAVIS:
            host = "localhost"
            port = 6379
        else:
            host, port = pg_container.run()

        yield host, port  # provide the fixture value

        if not IS_TRAVIS:
            pg_container.stop()


@pytest.fixture(scope="session")
def etcd():
    if os.environ.get("ETCD"):
        yield os.environ["ETCD"].split(":")
    else:
        yield etcd_container.run()
        etcd_container.stop()


@pytest.fixture(scope="session")
def es():
    if os.environ.get("ELASTICSEARCH"):
        yield os.environ["ELASTICSEARCH"].split(":")
    else:
        yield es_container.run()
        es_container.stop()


@pytest.fixture(scope="session")
def rabbitmq():
    if os.environ.get("RABBITMQ"):
        yield os.environ["RABBITMQ"].split(":")
    else:
        yield rabbitmq_container.run()
        rabbitmq_container.stop()


@pytest.fixture(scope="session")
def kafka():
    if os.environ.get("KAFKA"):
        yield os.environ["KAFKA"].split(":")
    else:
        yield kafka_container.run()
        kafka_container.stop()


@pytest.fixture(scope="session")
def minio():
    if os.environ.get("MINIO"):
        yield os.environ["MINIO"].split(":")
    else:
        if IS_TRAVIS:
            host = "localhost"
            port = 19000
        else:
            host, port = minio_container.run()

        yield host, port

        if not IS_TRAVIS:
            minio_container.stop()


@pytest.fixture(scope="session")
def mysql():
    if os.environ.get("MYSQL"):
        yield os.environ["MYSQL"].split(":")
    else:
        yield mysql_container.run()
        mysql_container.stop()


@pytest.fixture(scope="session")
def memcached():
    if os.environ.get("MEMCACHED"):
        host, port = os.environ["MEMCACHED"].split(":")
        yield host, port
    else:
        host, port = memcached_container.run()
        yield host, port
        memcached_container.stop()


@pytest.fixture(scope="session")
def stripe():
    if os.environ.get("STRIPE"):
        host, port = os.environ["STRIPE"].split(":")
        yield host, port
    else:
        host, port = stripe_container.run()
        yield host, port
        stripe_container.stop()


@pytest.fixture(scope="session")
def mosquitto() -> Generator[HostPort, None, None]:
    yield mosquitto_container.run()
    mosquitto_container.stop()
