from ._base import BaseImage


class MySQL(BaseImage):
    name = 'mysql'
    port = 3306

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


mysql_image = MySQL()
