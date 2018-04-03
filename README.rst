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
