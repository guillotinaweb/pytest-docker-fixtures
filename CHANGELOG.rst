1.3.16 (2023-03-24)
-------------------

- Use compatibile version of redis with arm support
  [vangheem]

1.3.15 (2022-11-17)
-------------------

- Set Redis image version to 6.2.6 for amd64 arch [albertnadal]


1.3.14 (2022-07-06)
-------------------

- Add stripe/stripemock image [jotare]


1.3.13 (2021-11-23)
-------------------

- Support for Apple Silicon images [bloodbare]


1.3.12 (2021-08-30)
-------------------

- Add support for remote docker daemons [sunbit]


1.3.11 (2020-09-30)
-------------------

- fix release

1.3.10 (2020-09-30)
-------------------

- Add memcached docker image [lferran]


1.3.9 (2020-07-10)
------------------

- Fix passing options to image configuration
  [gitcarbs]


1.3.8 (2020-07-02)
------------------

- Stop hardcoding db, user, and password in Postgresql.check()
  [marshalium]


1.3.7 (2020-05-04)
------------------

- Change psycopg2 dependency to psycopg2-binary


1.3.6 (2020-02-14)
------------------

- Update to working postgres image after upstream 9.6 change


1.3.5 (2019-10-01)
------------------

- minio: use random port (breaking change!)
  [masipcat]


1.3.4 (2019-09-04)
------------------

- Be able to override with env variables
  [vangheem]


1.3.3 (2019-08-14)
------------------

- Add support for MySQL
  [masipcat]


1.3.2 (2019-07-19)
------------------

- Fix: custom max_wait_s option should not be passed to docker images [lferran]

1.3.1 (2019-07-19)
------------------

- Allow configuring time to wait for image to be setup [lferran]


1.3.0 (2019-04-05)
------------------

- Be able to configure more of image
  [vangheem]

- Make sure ImportError is bubbled
  [vangheem]


1.2.10 (2019-02-28)
-------------------

- minio: configure a custom version of the image doesn't work
  [masipcat]
- minio: check() fails because Minio responds with status 403
  [masipcat]


1.2.9 (2019-01-09)
------------------

- Fix Minio returning port = None
  [masipcat]


1.2.8 (2019-01-03)
------------------

- Add support for Minio
  [masipcat]


1.2.7 (2018-11-19)
------------------

- ensure Kafka is available
  [ableeb]


1.2.6 (2018-11-15)
------------------

- Fix use of optional dependency
  [vangheem]


1.2.5 (2018-11-13)
------------------

- Add support for Kafka
  [ableeb]

1.2.4 (unreleased)
------------------

- Add support for RabbitMQ
  [davidonna]


1.2.3 (2018-06-10)
------------------

- bump


1.2.2 (2018-05-06)
------------------

- Fix es when using 6
  [vangheem]


1.2.1 (2018-05-05)
------------------

- Fix Elasticsearch image
  [vangheem]


1.2.0 (2018-05-05)
------------------

- Be able to configure custom docker images
  [vangheem]

1.1.0 (2018-04-03)
------------------

- Add Elasticsearch fixture
  [vangheem]


1.0.1 (2018-03-12)
------------------

- release


1.0.0 (2018-03-12)
------------------

- initial release
