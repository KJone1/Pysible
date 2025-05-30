from pysible.exceptions.task_exceptions import TaskFailedException
import pysible.utils.file_utils as files
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.utils.log_utils import Logger


@task_plugin(name="Setup Moonlander keyboard", section=Sections.SYSTEM)
def setup_moonlander() -> None:
    """Sets up udev rules for the ZSA Moonlander keyboard.

    This function copies a predefined udev rules file (`50-zsa.rules`) from
    the application's resources to the system's udev rules directory
    (`/etc/udev/rules.d/`). This allows the system to correctly recognize
    and configure the Moonlander keyboard.

    Side Effects:
        - Copies a file to a system directory (`/etc/udev/rules.d/`), which
          typically requires sudo privileges.
        - May trigger udev to reload rules, or a manual reload might be needed
          for changes to take effect.
        - Logs a success message or raises an exception on failure.

    Raises:
        TaskFailedException: If the `copy_resource` operation fails for any
                             reason (e.g., file not found in resources,
                             permission denied to write to the destination,
                             or other I/O errors).
    """
    udev_rules = "50-zsa.rules"
    rules_dir = "/etc/udev/rules.d/"
    try:
        _ = files.copy_resource(filename=udev_rules, dest=rules_dir)
        Logger.success(f"Copied {udev_rules} to {rules_dir}")
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg=f"Failed to copy {udev_rules}",
        )
