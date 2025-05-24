from pysible.config.settings import settings
from pysible.utils.log_utils import Logger
import sh
import pysible.utils.net_utils as net
import pysible.utils.package_utils as pkg
from pysible.utils.misc_utils import create_tmp_dir


def install_k9s(version:str):
    try:
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
        Logger.failure(f"Failed to set k9s permissions -> {e}")
    except sh.ErrorReturnCode as e:
        Logger.failure(f"DNF[{e.exit_code}] install failed -> {e.stderr}")
    except sh.CommandNotFound:
        Logger.failure(
            f"Error: Command 'dnf' not found. Is dnf installed and in the system PATH?",
        )
    except Exception as e:
        Logger.failure(f"Caught unexpected k9s error -> {e}")
