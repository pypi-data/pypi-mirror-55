import os
from urllib.parse import urlparse

import yaml

from . import exceptions
from .chart_museum import ChartMuseum
from .gcs import GCSBucket
from .repo import Repo

DEFAULT_REPO_FILE = "~/.helm/repository/repositories.yaml"


class Repositories:
    def __init__(self, file_path: str = DEFAULT_REPO_FILE):
        self.file_path = file_path
        with open(os.path.expanduser(file_path)) as repo_file:
            repos = yaml.safe_load(repo_file)
        self._repos = {}
        for repo in repos["repositories"]:
            repo_scheme = urlparse(repo["url"]).scheme
            if repo_scheme in ('http', 'https'):
                self._repos[repo["name"]] = ChartMuseum(**repo)
            elif repo_scheme == "gs":
                self._repos[repo["name"]] = GCSBucket(**repo)
            else:
                raise Exception("invalid scheme")

    def __repr__(self):
        return f"<deploy_py.helm.Repositories: {self.file_path}>"

    def get(self, name: str):
        try:
            return self._repos[name]
        except KeyError:
            raise exceptions.RepoNotFoundException(f"no repo found for: {name}")
