from .base import BaseImage
from .base import ContainerConfiguration


class CockroachDB(BaseImage):
    name: str = "cockroach"
    config: ContainerConfiguration = ContainerConfiguration(
        image="cockroachdb/cockroach",
        version="v1.1.7",
        options={
            "command": " ".join(
                [
                    "start --insecure",
                ]
            ),
            "publish_all_ports": False,
            "ports": {"26257/tcp": "26257"},
        },
    )

    def check(self):
        import psycopg2

        conn = cur = None
        try:
            conn = psycopg2.connect(
                f"dbname=guillotina user=root host={self.host} "
                f"port={self.get_port()}"
            )
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            cur.execute("SHOW DATABASES;")
            for result in cur.fetchall():
                if result[0] == "guillotina":
                    conn.close()
                    cur.close()
                    return True
            cur.execute("CREATE DATABASE IF NOT EXISTS guillotina;")
            cur.close()
            conn.close()
        except:  # noqa
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()
        return False


cockroach_image = CockroachDB()
