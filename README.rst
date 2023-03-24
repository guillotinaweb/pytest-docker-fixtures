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
- mysql (require to be installed with `pip install pytest-docker-fixtures[mysql]`)
- pg (require to be installed with `pip install pytest-docker-fixtures[pg]`)
- rabbitmq (require to be installed with `pip install pytest-docker-fixtures[rabbitmq]`)
- redis
- stripe (stripemock)

Configuring custom images
-------------------------

You can also configure custom images to use::

    from pytest_docker_fixtures import images
    images.configure(
        'elasticsearch',
        'docker.elastic.co/elasticsearch/elasticsearch-platinum', '6.2.4',
        env={},
        options={}
    )
