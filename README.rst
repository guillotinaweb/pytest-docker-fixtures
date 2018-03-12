Introduction
============

Provide various service pytest fixtures.


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
- pg
- cockroach
- etcd
