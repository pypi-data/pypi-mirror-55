import json
import os
import tarfile
from typing import List, NamedTuple

from hapi.chart.chart_pb2 import Chart
from hapi.services.tiller_pb2 import UpdateReleaseResponse
from jinja2 import Template
from pyhelm.chartbuilder import ChartBuilder
from pyhelm.tiller import Tiller

from . import exceptions
from .. import kube
from ..logger import get_logger
from .port_forwarding import PortForwarder
from .storage import Repositories, Repo

DEFAULT_REPO_FILE = "~/.helm/repository/repositories.yaml"
DEFAULT_TILLER_LABELS = {
    "app": "helm",
    "name": "tiller"
}
MODULE_PREFIX = "deploy.helm."


class _ChartKinds(NamedTuple):
    directory: str = "directory"
    repo: str = "repo"
    git: str = "git"


ChartKinds = _ChartKinds()


class Client:
    def __init__(self, tiller_namespace: str = "kube-system", repo_file: str = DEFAULT_REPO_FILE, verbosity: int = 0):
        self.logger = get_logger("deploy.helm.Client", level=verbosity)
        self.repos = Repositories(repo_file)
        self.repo_file = repo_file
        self.tiller_namespace = tiller_namespace
        self.kube = None

    @staticmethod
    def exclude_function(tarinfo):
        if ".helmignore" in tarinfo.name:
            return None
        else:
            return tarinfo

    def make_tarfile(self, output_filename: str, source_dir: str):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir), filter=self.exclude_function)

    def get_repo(self, repo_name: str) -> Repo:
        try:
            return self.repos.get(repo_name)
        except KeyError:
            raise exceptions.HelmRepoNotFoundError(repo_name, self.repo_file, [])

    def delete_chart(self, repo_name: str, chart_name: str, version: str):
        repo = self.get_repo(repo_name)
        repo.delete(chart_name, version)

    def package(self, name: str, version: str, src_dir: str, out_dir: str) -> str:
        self.logger.info(f"creating Helm chart {name}:{version}")
        out_name = os.path.join(os.path.expanduser(out_dir), f"{name}-{version}.tgz")
        self.make_tarfile(out_name, src_dir)
        return out_name

    def upload(self, repo_name: str, file_path: str, chart_name, version):
        repo = self.repos.get(repo_name)
        repo.upload(file_path, chart_name, version)

    def list(self, context) -> List[Chart]:
        if self.kube is None:
            self.kube = kube.Client(context)
        pod_name, port = self.kube.get_pod_name_and_port(self.tiller_namespace, DEFAULT_TILLER_LABELS, "tiller")
        with PortForwarder(pod_name, context, dest_port=port, namespace=self.tiller_namespace) as port:

            t = Tiller("localhost", port=port)
            releases = t.list_charts()
            return releases

    @staticmethod
    def build_chart(name: str, version: str, kind: str, location: str):
        chart_options = {
            "name": name,
            "version": version,
            "source": {
                "type": kind,
                "location": location
            }
        }
        return ChartBuilder(chart_options)

    def _format_values(self, values, context):
        pass

    def update_release(self, name: str, version: str, app_namespace: str, chart_path: str, kind: str,
                       context: str, dry_run: bool = False, values: dict = None) -> (UpdateReleaseResponse, bool):
        if self.kube is None:
            self.kube = kube.Client(context)
        if values is None:
            values = {}

        tmpl = Template(json.dumps(values))
        values = json.loads(tmpl.render(app=name, new_version=version))

        chart = self.build_chart(name, version, kind, chart_path)
        pod_name, tiller_port = self.kube.get_pod_name_and_port(self.tiller_namespace, DEFAULT_TILLER_LABELS, "tiller")
        # with PortForwarder(pod_name, context, dest_port=tiller_port, namespace=self.tiller_namespace) as port:
        #     self.logger.debug(
        #         f"port forwarding from localhost:{port} -> {self.tiller_namespace}:{pod_name}:{tiller_port}"
        #     )
        #     tiller = Tiller("tiller-deploy.kube-system.svc.cluster.local", port=44314)
        #     self.logger.debug("update_release args:")
        #     self.logger.debug({
        #         "chart": chart.get_helm_chart().metadata.name,
        #         "namespace": app_namespace,
        #         "dry_run": dry_run,
        #         "name": name,
        #         "install": True,
        #         "values": values,
        #     })
        #     try:
        #         resp = tiller.update_release(
        #             chart.get_helm_chart(),
        #             namespace=app_namespace,
        #             dry_run=dry_run,
        #             name=name,
        #             install=True,
        #             values=values,
        #         )
        #         if resp.release.info.status.code == resp.release.info.status.FAILED:
        #             self.logger.error(f"release failed: {resp.release.info.description}")
        #             return resp,  False
        #         else:
        #             self.logger.info(
        #                 f"release status is {resp.release.info.status.Code.Name(resp.release.info.status.code)}"
        #             )
        #             self.logger.debug(resp.release.info)
        #     except Exception as err:
        #         self.logger.error(f"error updating release: {err}")
        #         return None, False
        # return resp, True
        tiller = Tiller("tiller-deploy.kube-system.svc.cluster.local", port=44134)
        self.logger.debug("update_release args:")
        self.logger.debug({
            "chart": chart.get_helm_chart().metadata.name,
            "namespace": app_namespace,
            "dry_run": dry_run,
            "name": name,
            "install": True,
            "values": values,
        })
        try:
            resp = tiller.update_release(
                chart.get_helm_chart(),
                namespace=app_namespace,
                dry_run=dry_run,
                name=name,
                install=True,
                values=values,
            )
            if resp.release.info.status.code == resp.release.info.status.FAILED:
                self.logger.error(f"release failed: {resp.release.info.description}")
                return resp, False
            else:
                self.logger.info(
                    f"release status is {resp.release.info.status.Code.Name(resp.release.info.status.code)}"
                )
                self.logger.debug(resp.release.info)
        except Exception as err:
            self.logger.error(f"error updating release: {err}")
            return None, False
        return resp, True

    def update_index(self, chart_dir: str, repo_name: str):
        repo = self.get_repo(repo_name)
        self.logger.info("WIP: Updating Helm index file...")
        self.logger.info("WIP: Updating Helm chart _repos...")
