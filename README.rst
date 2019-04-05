Introduction
============

Provide various service pytest fixtures.


Install
-------

`pip install pytest-docker-fixtures`

Usages
------

In your conftest.py, add the following:

    pytest_plugins = ['pytest_docker_fixtures']


And to use the fixtures:

    def test_foobar(redis):
        pass


Available fixtures
------------------

PRs welcome!

- redis
- etcd
- pg(require to be installed with `pip install pytest-docker-fixtures[pg]`)
- cockroach(require to be installed with `pip install pytest-docker-fixtures[pg]`)
- es
- cockroach
- kafka
- minio
- rabbitmq


Configuring custom images
-------------------------

You can also configure custom images to use::

    from pytest_docker_fixtures import images
    images.configure(
        'elasticsearch',
        'docker.elastic.co/elasticsearch/elasticsearch-platinum', '6.2.4',
        env={},
        options={})
