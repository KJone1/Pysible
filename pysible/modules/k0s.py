import sh

from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger


@task_plugin(name="Install k0s", section=Sections.SOFTWARE)
def install_k0s() -> None:
    """Installs k0s, a lightweight Kubernetes distribution.

    This function performs the following steps:
    1. Downloads and executes the official k0s installation script using curl
       and sh. This script typically installs the k0s binary.
    2. Runs the k0s command to install a single-node controller, forcing
       the installation if a previous one exists.
    3. Logs informational messages at the start of the process.

    Side Effects:
        - Downloads and executes an external script from the internet.
        - Installs k0s binaries and related files onto the system.
        - May create or modify system services for k0s.
        - Requires sudo privileges for installation.
        - Logs the start of the installation.

    Raises:
        TaskFailedException: If any of the shell commands (curl, k0s install)
                             fail with a non-zero exit code, or if any other
                             unexpected exception occurs during the process.
    """
    Logger.info("Starting to install k0s...")
    try:
        sh.bash("curl -sSLf https://get.k0s.sh | sudo sh")
        sh.bash("k0s install controller --force --single")
    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Failed to install k0s",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught unexpected k0s error",
        )
