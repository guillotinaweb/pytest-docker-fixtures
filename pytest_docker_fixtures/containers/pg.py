from ._base import BaseImage


class Postgresql(BaseImage):
    name = 'postgresql'
    port = 5432

    def check(self):
        import psycopg2
        try:
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
