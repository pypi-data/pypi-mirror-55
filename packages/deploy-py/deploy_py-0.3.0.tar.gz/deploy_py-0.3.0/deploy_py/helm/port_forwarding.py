import socket
import subprocess
import sys


class PortForwarder:
    def __init__(self, pod_name: str, context: str,
                 src_port: int = 8000, dest_port: int = 44134, namespace: str = "kube-system"):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.src_port = src_port
        self.pod_name = pod_name
        self.dest_port = dest_port
        self.namespace = namespace
        self.context = context
        self.fwd = None

    def __enter__(self):
        try:
            if not self.src_port:
                self.tcp.bind(('', 0))
                _, self.src_port = self.tcp.getsockname()
            self.fwd = subprocess.Popen([
                "kubectl",
                "port-forward",
                self.pod_name,
                "-n", self.namespace,
                "--context", self.context,
                f"{self.src_port}:{self.dest_port}"
            ],
                stdout=subprocess.PIPE,
                shell=True
            )
            return self.src_port
        except:
            if self.__exit__(*sys.exc_info()):
                pass
            else:
                raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.tcp.close()
            self.fwd.terminate()
        except AttributeError:
            pass
        if any((self, exc_type, exc_val, exc_tb)):
            return False
        return True
