import requests
import sh

import pysible.utils.net_utils as net
import pysible.utils.package_utils as pkg
from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir


@task_plugin(name="Install k9s", section=Sections.SOFTWARE)
def install_k9s():
    """Installs k9s, a terminal-based UI for Kubernetes clusters.

    This function performs the following steps:
    1. Fetches the latest version tag of k9s from the "derailed/k9s"
       GitHub repository.
    2. Constructs the download URL for the Linux amd64 RPM package.
    3. Creates a temporary directory for the download.
    4. Downloads the k9s RPM package.
    5. Installs the RPM package using `pysible.utils.package_utils.install_package`.
    6. Logs success or failure messages.

    Side Effects:
        - Creates a temporary directory.
        - Downloads a file from the internet.
        - Installs an RPM package, which modifies the system and requires
          sudo privileges.
        - Logs information about the process.

    Raises:
        TaskFailedException: If any step in the process fails. This includes
                             errors during version fetching (network issues, API
                             changes), file download, RPM installation (DNF errors,
                             command not found), or any other unexpected Python
                             exceptions (OSError, ValueError, KeyError).
    """
    try:
        version = net.get_latest_version_from_github(
            repo_owner="derailed", repo_name="k9s"
        )
        k9s_url = f"https://github.com/derailed/k9s/releases/download/{version}/k9s_Linux_amd64.rpm"
        k9s_tmp_dir_name = "k9s"
        k9s_tmp_dir_path = f"{settings.TMP_DIR}/{k9s_tmp_dir_name}"

        Logger.info(f"Starting to install k9s {version}...")
        create_tmp_dir(name=k9s_tmp_dir_name)
        local_rpm_name = f"{k9s_tmp_dir_path}/k9s-{version}.rpm"
        net.wget(url=k9s_url, dest=local_rpm_name)
        _ = pkg.install_package(local_rpm_name)
        Logger.success(f"Installed k9s {version}")

    except requests.exceptions.RequestException as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error fetching release information",
        )
    except (OSError, ValueError) as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to set k9s permissions",
        )
    except KeyError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="'tag_name' not found in the API response",
        )
    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg=f"DNF[{e.exit_code}] install failed",
        )
    except sh.CommandNotFound as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error: Command 'dnf' not found. Is dnf installed and in the system PATH?",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught unexpected k9s error",
        )
