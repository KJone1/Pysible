import requests
import sh

import pysible.utils.net_utils as net
import pysible.utils.package_utils as pkg
from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir


@task_plugin(
    name="Install k9s", section=Sections.SOFTWARE
)
def install_k9s():
    try:
        version = net.get_latest_version_from_github(repo_owner="derailed",repo_name="k9s")
        k9s_url = f"https://github.com/derailed/k9s/releases/download/{version}/k9s_Linux_amd64.rpm"
        k9s_tmp_dir_name = "k9s"
        k9s_tmp_dir_path = f"{settings.TMP_DIR}/{k9s_tmp_dir_name}"

        Logger.info(f"Starting to install k9s {version}...")
        create_tmp_dir(name=k9s_tmp_dir_name)
        local_rpm_name = f"{k9s_tmp_dir_path}/k9s-{version}.rpm"
        net.wget(url=k9s_url, dest=local_rpm_name)
        _ = pkg.install_package(local_rpm_name)
        Logger.success(f"Installed k9s {version}")

    except (OSError, ValueError) as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to set k9s permissions",
        )
    except requests.exceptions.RequestException as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error fetching release information",
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
