import ntpath
from urllib.parse import urlparse

import yaml
from google.cloud import storage
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

from .repo import Repo


class GCSBucket(Repo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        credentials = service_account.Credentials.from_service_account_file("/home/jenkins/agent/workspace/dind-testing/xray/creds.json")
        self.client = storage.Client(credentials=credentials)
        repo_url_parsed = urlparse(self.url)
        self.bucket_name = repo_url_parsed.netloc

    def _index_entry(self, name, version, digest):
        return {
            "apiVersion": "v1",
            "created": self.get_timestamp(),
            "description": "",
            "digest": digest,
            "name": name,
            "urls": [
                f"{self.url}/{name}-{version}.tgz"
            ],
            "version": version
        }

    def _get_index(self, ):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob("index.yaml")

        return yaml.safe_load(blob.download_as_string())

    def _update_index(self, index):
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob("index.yaml")
        blob.upload_from_string(yaml.safe_dump(index))

    def add_entry(self, name, version, digest):
        index = self._get_index()
        entries = index["entries"].get(name)
        if not entries:
            index["entries"][name] = []
        index["entries"][name].append(self._index_entry(name, version, digest))
        self._update_index(index)

    def remove_entry(self, name, version):
        index = self._get_index()
        entries = index["entries"].get(name)
        if not entries:
            return
        index["entries"][name] = [entry for entry in index["entries"][name] if entry["verison"] != version]
        self._update_index(index)

    def delete(self, chart_name: str, version: str):
        repo_url_parsed = urlparse(self.url)
        bucket_name = repo_url_parsed.netloc

        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(f"{chart_name}-{version}.tgz")
        try:
            blob.delete()
        except NotFound:
            pass

    def upload(self, file_path: str, chart_name: str, version: str):
        repo_url_parsed = urlparse(self.url)
        bucket_name = repo_url_parsed.netloc

        bucket = self.client.get_bucket(bucket_name)
        blob = bucket.blob(ntpath.basename(file_path))
        blob.upload_from_filename(file_path)
        self.add_entry(chart_name, version, self.get_file_digest(file_path))
