from ._base import BaseImage


class Postgresql(BaseImage):
    name = 'postgresql'
    port = 5432

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(dict(
            environment={
                'POSTGRES_PASSWORD': '',
                'POSTGRES_DB': 'guillotina',
                'POSTGRES_USER': 'postgres'
            }
        ))
        return image_options

    def check(self):
        try:
            import psycopg2
            conn = psycopg2.connect(
                f"dbname=guillotina user=postgres host={self.host} "
                f"port={self.get_port()}")
            cur = conn.cursor()
            cur.execute("SELECT 1;")
            cur.fetchone()
            cur.close()
            conn.close()
            return True
        except: # noqa
            conn = None
            cur = None
        return False


pg_image = Postgresql()
