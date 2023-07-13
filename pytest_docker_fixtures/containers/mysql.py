from .base import BaseContainer
from .base import ContainerConfiguration


class MySQL(BaseContainer):
    name: str = "mysql"
    config: ContainerConfiguration = ContainerConfiguration(
        image="mysql",
        version="5.7",
        port=3306,
        env={"MYSQL_ALLOW_EMPTY_PASSWORD": "yes"},
    )

    def check(self):
        import mysql.connector

        conn = None
        cur = None

        try:
            conn = mysql.connector.connect(
                host=self.host,
                port=self.get_port(),
                user="root",
                use_pure=True,
            )

            try:
                cur = conn.cursor()
                cur.execute("SELECT 1;")
                cur.fetchone()
            finally:
                if cur:
                    cur.close()

            return True
        except Exception:
            return False
        finally:
            if conn:
                conn.close()


mysql_container = MySQL()
