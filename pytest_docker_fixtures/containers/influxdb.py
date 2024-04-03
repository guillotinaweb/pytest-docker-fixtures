from ._base import BaseImage

import requests


class InfluxDB(BaseImage):
    name = 'influxdb'
    port = 8086

    def check(self):
        port = self.get_port(8086)
        url = f"http://{self.host}:{port}/health"
        try:
            options = self.get_image_options()
            admin_user = options.get("environment", "admin").get("INFLUXDB_ADMIN_USER", "admin")  # noqa
            token = options["environment"]["INFLUXDB_ADMIN_USER_TOKEN"]
            session = requests.Session()
            session.auth = (admin_user, token)
            resp = requests.get(url)
            if resp.status_code == 200 and resp.json()["status"] == "pass":
                return True
        except Exception:
            return False


influxdb_image = InfluxDB()
