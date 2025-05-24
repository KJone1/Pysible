import sh

import pysible.utils.file_utils as files
import pysible.utils.net_utils as net
from pysible.config.settings import settings
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir


def install_nerdctl(version: str = "2.0.0") -> None:
    nerdctl_url = f"https://github.com/containerd/nerdctl/releases/download/v{version}/nerdctl-{version}-linux-amd64.tar.gz"
    nerdctl_bin_dest = "/usr/local/bin/nerdctl"

    Logger.info("Starting to install nerdctl...")
    try:

        create_tmp_dir(name="nerdctl")

        tmp_dir = f"{settings.TMP_DIR}/nerdctl"
        local_tar_name = f"{tmp_dir}/nerd-{version}.tar.gz"
        net.wget(url=nerdctl_url, dest=local_tar_name)

        files.untar(input_tar=local_tar_name, output=tmp_dir, strip=False)
        files.copy(source=f"{tmp_dir}/nerdctl", dest=nerdctl_bin_dest)
        _ = files.copy_resource(
            filename="nerdctl.toml",
            dest="/etc/nerdctl/nerdctl.toml",
            sudo=True,
        )
        files.set_file_permissions(nerdctl_bin_dest, "555")
        Logger.success(f"Installed nerdctl {version}")
    except (OSError, ValueError) as e:
        Logger.failure(f"Failed to set nerdctl permissions -> {e}")
    except (sh.ErrorReturnCode, FileNotFoundError) as e:
        Logger.failure(f"Failed to copy nerdctl.toml -> {e}")
    except Exception as e:
        Logger.failure(f"caught unexpected nerdctl error -> {e}")
