import json
import os
import requests
import sh
import pysible.utils.file_utils as files
import pysible.utils.net_utils as net
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger


def _download_kubectl(version: str) -> str:

    kubectl_download_url = f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"
    kubectl_path = "/usr/local/bin/kubectl"

    if os.path.exists(kubectl_path):
        kubectl = sh.Command(kubectl_path)
        installed_version = kubectl("version", "--client", "-o=json",_ok_code=[0, 1])
        if installed_version:
            version_data = json.loads(str(installed_version))
            installed_version_str: str = version_data.get("clientVersion", {}).get(
                "gitVersion"
            )
            Logger.info(
                f"Currently installed version: {installed_version_str}, latest: {version}"
            )
            if installed_version_str == version:
                Logger.info(
                    "Skipping download"
                )
    else:
        Logger.info(f"Downloading kubectl {version}")
        net.wget(url=kubectl_download_url, dest=kubectl_path)
    return kubectl_path


@task_plugin(name="Install kubectl", section=Sections.SOFTWARE)
def install_kubectl():
    version_url = "https://dl.k8s.io/release/stable.txt"
    try:
        response = requests.get(version_url, timeout=15)
        response.raise_for_status()
        version = response.text.strip()

        path = _download_kubectl(version)
        files.set_file_permissions(path, "555")
    except requests.HTTPError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to download kubectl",
        )
    except RuntimeError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught RuntimeError while downloading kubectl",
        )
    except PermissionError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Encounter permission error while downloading kubectl",
        )
    except requests.exceptions.RequestException as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error fetching Kubernetes version",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught unexpected error while installing kubectl",
        )
