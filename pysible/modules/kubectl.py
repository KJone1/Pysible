import requests

import pysible.utils.file_utils as files
import pysible.utils.net_utils as net
from pysible.utils.log_utils import Logger


def _download_kubectl(version: str) -> str:
    Logger.info(f"Downloading kubectl {version}")

    kubectl_ver = f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"
    kubectl_dest = "/usr/local/bin/kubectl"

    net.wget(url=kubectl_ver, dest=kubectl_dest)
    return kubectl_dest


def install_kubectl():
    version_url = "https://dl.k8s.io/release/stable.txt"
    try:
        response = requests.get(version_url)
        response.raise_for_status()
        version = response.text.strip()

        path = _download_kubectl(version)
        files.set_file_permissions(path, "555")
        Logger.success(f"Installed kubectl {version}")
    except requests.HTTPError as e:
        raise Logger.failure(f"Failed to download kubectl -> {e}")
    except requests.exceptions.RequestException as e:
        Logger.failure(f"Error fetching Kubernetes version -> {e}")
    except Exception as e:
        Logger.failure(f"Caught unexpected error while installing kubectl -> {e}")
