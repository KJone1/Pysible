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
    """Downloads the kubectl binary if not already present or if outdated.

    Checks if kubectl is already installed at /usr/local/bin/kubectl. If it is,
    compares its version with the provided target version. If the installed
    version matches the target version, the download is skipped. Otherwise, or
    if kubectl is not found, it downloads the specified version of kubectl
    from the official Kubernetes release URL.

    Args:
        version: The desired version string of kubectl to download (e.g., "v1.23.0").

    Returns:
        The path to the kubectl binary (/usr/local/bin/kubectl).

    Side Effects:
        - May download a file from the internet.
        - Writes the downloaded file to /usr/local/bin/kubectl, potentially
          overwriting an existing file. This requires sudo privileges if the
          current user does not have write access.
        - Logs informational messages about the current version and download process.

    Raises:
        ValueError: If the URL for downloading kubectl is invalid (though this is
                    handled by net.wget).
        requests.exceptions.RequestException: If downloading fails (handled by net.wget).
        sh.ErrorReturnCode: If checking the version of an existing kubectl fails.
    """
    kubectl_download_url = (
        f"https://dl.k8s.io/release/{version}/bin/linux/amd64/kubectl"
    )
    kubectl_path = "/usr/local/bin/kubectl"

    if os.path.exists(kubectl_path):
        kubectl = sh.Command(kubectl_path)
        installed_version = kubectl("version", "--client", "-o=json", _ok_code=[0, 1])
        if installed_version:
            version_data = json.loads(str(installed_version))
            installed_version_str: str = version_data.get("clientVersion", {}).get(
                "gitVersion"
            )
            Logger.info(
                f"Currently installed version: {installed_version_str}, latest: {version}"
            )
            if installed_version_str == version:
                Logger.info("Skipping download")
    else:
        Logger.info(f"Downloading kubectl {version}")
        net.wget(url=kubectl_download_url, dest=kubectl_path)
    return kubectl_path


@task_plugin(name="Install kubectl", section=Sections.SOFTWARE)
def install_kubectl():
    """Installs the latest stable version of kubectl.

    This function performs the following steps:
    1. Fetches the latest stable version string from the Kubernetes release server.
    2. Calls `_download_kubectl` to download the kubectl binary, if necessary.
    3. Sets the downloaded kubectl binary's permissions to '555' (read and execute
       for all users).

    Side Effects:
        - Interacts with the network to fetch the latest version string.
        - Calls `_download_kubectl` which has its own side effects (downloading
          files, writing to the file system).
        - Modifies file permissions on /usr/local/bin/kubectl, typically
          requiring sudo privileges.

    Raises:
        TaskFailedException: If fetching the version string fails, if downloading
                             or setting permissions for kubectl fails (due to HTTP
                             errors, permission errors, runtime errors, or other
                             request exceptions), or any other unexpected error occurs.
    """
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
