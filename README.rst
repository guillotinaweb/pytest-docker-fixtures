Introduction
============

Provide various service pytest fixtures.


Install
-------

`pip install pytest-docker-fixtures`

Usages
------

In your conftest.py, add the following: ::

    pytest_plugins = ['pytest_docker_fixtures']

And to use the fixtures: ::

    def test_foobar(redis):
        pass


Available fixtures
------------------

PRs welcome!

- cockroach (require to be installed with `pip install pytest-docker-fixtures[pg]`)
- es (elasticsearch)
- etcd
- kafka (require to be installed with `pip install pytest-docker-fixtures[kafka]`)
- memcached (require to be installed with `pip install pytest-docker-fixtures[memcached]`)
- minio
- mosquitto (MQTT)
- mysql (require to be installed with `pip install pytest-docker-fixtures[mysql]`)
- pg (require to be installed with `pip install pytest-docker-fixtures[pg]`)
- rabbitmq (require to be installed with `pip install pytest-docker-fixtures[rabbitmq]`)
- redis
- stripe (stripemock)

Configuring custom container
-------------------------

You can also configure custom container to use::

    Example: Bind mosquitto to fixed port

    from pytest_docker_fixtures.containers.mosquitto import mosquitto_container

    mosquitto_container.config.options.update(
        {
            "ports": {"1883/tcp": 1883},
        }
    )
