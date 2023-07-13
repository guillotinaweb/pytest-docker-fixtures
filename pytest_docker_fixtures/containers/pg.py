from .base import BaseImage
from .base import ContainerConfiguration


class Postgresql(BaseImage):
    name: str = "postgresql"
    config: ContainerConfiguration = ContainerConfiguration(
        image="postgres",
        version="9.6.16",
        port=5432,
        env={
            "POSTGRES_PASSWORD": "",
            "POSTGRES_DB": "guillotina",
            "POSTGRES_USER": "postgres",
        },
    )

    def check(self):
        import psycopg2

        try:
            env = self.get_image_options()["environment"]

            conn_string = (
                f"dbname={env['POSTGRES_DB']} user={env['POSTGRES_USER']} "
                f"host={self.host} port={self.get_port()}"
            )
            if env.get("POSTGRES_PASSWORD"):
                conn_string += f" password={env['POSTGRES_PASSWORD']}"

            conn = psycopg2.connect(conn_string)
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            cur.fetchone()
            cur.close()
            conn.close()
            return True
        except:  # noqa
            conn = None
            cur = None
        return False


pg_image = Postgresql()
