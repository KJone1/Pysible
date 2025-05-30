import sh

from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.file_utils import copy_resource
from pysible.utils.log_utils import Logger


@task_plugin(name="Setup sudoers file", section=Sections.SYSTEM)
def setup_sudoers():
    """Validates and installs a custom sudoers configuration file.

    This function performs the following steps:
    1. Defines the source path of the custom sudoers file (from application
       resources) and the destination path (`/etc/sudoers.d/kj`).
    2. Validates the syntax of the source sudoers file using `visudo -c -f`.
    3. If validation is successful, copies the source file to the system's
       sudoers.d directory. This operation requires sudo privileges.
    4. Logs the copy operation.

    Side Effects:
        - Runs `visudo` which checks sudoers file syntax.
        - Copies a file to `/etc/sudoers.d/`, which modifies system
          configuration and requires sudo privileges.
        - Can alter user privileges on the system based on the content of the
          copied sudoers file.
        - Logs information about the process.

    Raises:
        TaskFailedException: If `visudo` validation fails (sh.ErrorReturnCode),
                             if the source sudoers file is not found (FileNotFoundError),
                             or if `copy_resource` fails (e.g., permission issues,
                             though these are often caught as sh.ErrorReturnCode by
                             the underlying sudo operation in copy_resource).
    """
    sudoers_file_name = f"{settings.RESOURCES_DIR}/kj"
    sudoers_path = "/etc/sudoers.d/kj"
    try:
        sh.visudo("-c", "-f", sudoers_file_name)
        _ = copy_resource(filename=sudoers_file_name, dest=sudoers_path, sudo=True)
        Logger.info(f"Copied {sudoers_file_name} to {sudoers_path}")
    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error validating sudoers file",
        )
    except FileNotFoundError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Sudoers file not found",
        )
