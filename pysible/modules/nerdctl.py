import sh
from requests import HTTPError

import pysible.utils.file_utils as files
import pysible.utils.net_utils as net
from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir


@task_plugin(name="Install nerdctl", section=Sections.SOFTWARE)
def install_nerdctl() -> None:
    """Installs nerdctl, a Docker-compatible CLI for containerd.

    This function performs the following steps:
    1. Fetches the latest version of nerdctl from the "containerd/nerdctl"
       GitHub repository.
    2. Constructs the download URL for the Linux amd64 tarball.
    3. Creates a temporary directory for the download.
    4. Downloads the nerdctl tarball.
    5. Extracts the tarball into the temporary directory.
    6. Copies the 'nerdctl' binary to /usr/local/bin.
    7. Copies a default configuration file (`nerdctl.toml`) from resources
       to /etc/nerdctl/nerdctl.toml.
    8. Sets execute permissions ('555') on the nerdctl binary.
    9. Logs success or various failure messages.

    Side Effects:
        - Creates a temporary directory.
        - Downloads a file from the internet.
        - Extracts a tarball to the temporary directory.
        - Copies files to system directories (/usr/local/bin, /etc/nerdctl),
          which typically requires sudo privileges.
        - Modifies file permissions, typically requiring sudo privileges.
        - Logs information about the process.

    Raises:
        TaskFailedException: If any step in the process fails. This includes
                             errors during version fetching, download (HTTPError),
                             file operations (OSError, ValueError, sh.ErrorReturnCode,
                             FileNotFoundError), or any other unexpected Python exception.
    """
    version = net.get_latest_version_from_github(
        repo_owner="containerd", repo_name="nerdctl"
    )
    nerdctl_url = f"https://github.com/containerd/nerdctl/releases/download/{version}/nerdctl-{version[1:]}-linux-amd64.tar.gz"
    nerdctl_bin_dest = "/usr/local/bin/nerdctl"
    Logger.info(f"Starting to install nerdctl {version}...")
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
    except HTTPError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to download nerdctl",
        )
    except (OSError, ValueError) as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to set nerdctl permissions",
        )
    except (sh.ErrorReturnCode, FileNotFoundError) as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to copy nerdctl.toml",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught unexpected nerdctl error",
        )
