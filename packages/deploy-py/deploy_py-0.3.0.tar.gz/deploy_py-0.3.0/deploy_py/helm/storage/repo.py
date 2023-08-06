import hashlib
import time
from datetime import datetime


class Repo:
    def __init__(self, **kwargs):
        self.ca_file = kwargs.get("caFile")
        self.cache = kwargs.get("cache")
        self.cert_file = kwargs.get("certFile")
        self.key_file = kwargs.get("keyFile")
        self.name = kwargs.get("name")
        self.password = kwargs.get("password")
        self.url = kwargs.get("url")
        self.username = kwargs.get("username")

    def __repr__(self) -> str:
        return f"<deploy_py.helm.Repo: {self.name}>"

    def get_file_digest(self, file_path):
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def get_timestamp(self):
        dt = datetime.now()
        ts = dt.strftime("%Y-%m-%dT%H:%M:%S%f")
        off_set = int(time.localtime().tm_gmtoff / 60 / 60)
        is_negative = off_set < 0
        return f"{ts}{'-' if is_negative else ''}{str(abs(off_set)).zfill(2)}:00"

    def delete(self, chart_name: str, version: str):
        raise NotImplemented

    def upload(self, file_path: str, chart_name: str, version: str):
        raise NotImplemented
