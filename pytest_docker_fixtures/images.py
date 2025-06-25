import platform

settings = {
    "cockroach": {
        "image": "cockroachdb/cockroach",
        "version": "v1.1.7",
        "options": {
            "command": " ".join(
                [
                    "start --insecure",
                ]
            ),
            "publish_all_ports": False,
            "ports": {"26257/tcp": "26257"},
        },
    },
    "elasticsearch": {
        "image": "elasticsearch",
        "version": "5.2.0",
        "env": {
            "cluster.name": "docker-cluster",
            "ES_JAVA_OPTS": "-Xms512m -Xmx512m",
            "xpack.security.enabled": "false",
        },
        "options": {"cap_add": ["IPC_LOCK"], "mem_limit": "1g"},
    },
    "etcd": {"image": "quay.io/coreos/etcd", "version": "v3.2.0-rc.0"},
    "kafka": {
        "image": "spotify/kafka",
        "version": "latest",
        "env": {"ADVERTISED_PORT": "9092", "ADVERTISED_HOST": "0.0.0.0"},
        "options": {"ports": {"9092": "9092", "2181": "2181"}},
    },
    "memcached": {
        "image": "memcached",
        "version": "1.6.7",
    },
    "minio": {
        "image": "minio/minio",
        "version": "latest",
        "env": {
            "MINIO_ACCESS_KEY": "x" * 10,
            "MINIO_SECRET_KEY": "x" * 10,
        },
        "options": {
            "cap_add": ["IPC_LOCK"],
            "mem_limit": "200m",
            "command": "server /export",
        },
    },
    "mysql": {
        "image": "mysql",
        "version": "5.7",
        "env": {"MYSQL_ALLOW_EMPTY_PASSWORD": "yes"},
    },
    "postgresql": {
        "image": "postgres",
        "version": "9.6.16",
        "env": {
            "POSTGRES_PASSWORD": "",
            "POSTGRES_DB": "guillotina",
            "POSTGRES_USER": "postgres",
        },
    },
    "rabbitmq": {"image": "rabbitmq", "version": "3.7.8"},
    "redis": {
        "image": "redis",
        "version": "7.0.10",
        "options": {"cap_add": ["IPC_LOCK"], "mem_limit": "200m"},
    },
    "valkey": {
        "image": "valkey/valkey",
        "version": "8.1.2",
        "options": {"cap_add": ["IPC_LOCK"], "mem_limit": "200m"},
    },
    "stripe": {
        "image": "stripe/stripe-mock",
        "version": "v0.136.0",
        "options": {
            "ports": {
                "12111": "12111",  # HTTP (default)
                "12112": "12112",  # HTTPS
            }
        },
    },
    "emqx": {
        "image": "emqx",
        "version": "5.5.1"
    },
    "influxdb": {
        "image": "bitnami/influxdb",
        "version": "2.7.5",  # V2
        "env": {
            "INFLUXDB_ADMIN_USER_PASSWORD": "adminadmin",
            "INFLUXDB_ADMIN_USER_TOKEN": "admin",  # Can be used as basic auth
            "INFLUXDB_USER_BUCKET": "foo-bucket",
            "INFLUXDB_DB": "foo-database",
            "INFLUXDB_ADMIN_ORG": "foo-org"
        }
    }
}


def get_image(name):
    image = settings[name]
    return image["image"] + ":" + image["version"]


def configure(
    name, image=None, version=None, full=None, env=None, options=None, max_wait_s=None
):
    if full is not None:
        image, _, version = full.partition(":")
    if image is not None:
        settings[name]["image"] = image
    if version is not None:
        settings[name]["version"] = version
    if options is not None:
        settings[name]["options"] = options
    if env is not None:
        if "env" not in settings[name]:
            settings[name]["env"] = {}
        settings[name]["env"].update(env)
    if max_wait_s:
        settings[name]["max_wait_s"] = max_wait_s


def get_env(name):
    image = settings[name]

    return image.get("env") or {}


def get_max_wait_s(name):
    # Default to 30 seconds
    image = settings[name]
    return image.get("max_wait_s") or 30


def get_options(name):
    image = settings[name]
    return image.get("options") or {}
