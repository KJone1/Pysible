import sh

from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.file_utils import untar
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir, sudo_run
from pysible.utils.net_utils import wget


@task_plugin(name="Install Tomb", section=Sections.SOFTWARE, params={"version": "2.11"})
def install_tomb(version: str):
    """Installs Tomb, a tool for creating encrypted file storage.

    This function downloads a specific version of Tomb from its GitHub
    repository, extracts it, and then runs `make install` to install it
    on the system.

    Args:
        version: The version string of Tomb to install (e.g., "2.11").
                 This version is specified in the `@task_plugin` decorator's
                 params and passed by the Pysible core.

    Side Effects:
        - Creates a temporary directory.
        - Downloads a tarball from the internet.
        - Extracts the tarball in the temporary directory.
        - Runs `sudo make install`, which copies files to system locations
          (e.g., /usr/local/bin, /usr/local/share/man) and requires sudo
          privileges.
        - Logs information about the process, including success or failure.

    Raises:
        TaskFailedException: If any step of the process fails, including
                             download errors, extraction errors, `make install`
                             returning a non-zero exit code (sh.ErrorReturnCode),
                             or any other unexpected Python exception.
    """
    tmp_dir_name = "tomb"
    tmp_dir_path = f"{settings.TMP_DIR}/{tmp_dir_name}"
    url = f"https://github.com/dyne/tomb/archive/refs/tags/v{version}.tar.gz"
    file_dest = f"{tmp_dir_path}/{version}.tar.gz"

    Logger.info("Starting to install Tomb...")
    try:
        create_tmp_dir(name=tmp_dir_name)
        wget(url=url, dest=file_dest)
        untar(input_tar=file_dest, output=tmp_dir_path, strip=True)
        sudo_run("make", "install", _cwd=tmp_dir_path, _out="/dev/null")
        Logger.success(f"Installed Tomb {version}")
    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Encounter an ErrorReturnCode when tried to install Tomb",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Encounter an error when tried to install Tomb",
        )
