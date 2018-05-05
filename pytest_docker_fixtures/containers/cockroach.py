from ._base import BaseImage


class CockroachDB(BaseImage):
    name = 'cockroach'
    port = 26257

    def get_image_options(self):
        image_options = super().get_image_options()
        image_options.update(dict(
            command=' '.join([
                'start --insecure',
            ]),
            publish_all_ports=False,
            ports={
                f'26257/tcp': '26257'
            }
        ))
        return image_options

    def check(self):
        conn = cur = None
        try:
            import psycopg2
            conn = psycopg2.connect(
                f"dbname=guillotina user=root host={self.host} "
                f"port={self.get_port()}")
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            cur.execute('SHOW DATABASES;')
            for result in cur.fetchall():
                if result[0] == 'guillotina':
                    conn.close()
                    cur.close()
                    return True
            cur.execute("CREATE DATABASE IF NOT EXISTS guillotina;")
            cur.close()
            conn.close()
        except: # noqa
            if conn is not None:
                conn.close()
            if cur is not None:
                cur.close()
        return False


cockroach_image = CockroachDB()
