import re

from sh import ErrorReturnCode

from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


def _update_sddm_theme(config_file_path: str, theme_name: str) -> None:
    """Updates the SDDM theme in a given SDDM configuration file.

    It reads the specified configuration file, searches for a line starting
    with "Current=", and replaces its value with the provided `theme_name`.
    Other lines are written back unchanged.

    Args:
        config_file_path: The absolute path to the SDDM configuration file
                          (e.g., "/etc/sddm.conf.d/kde_settings.conf").
        theme_name: The name of the SDDM theme to set as current.

    Side Effects:
        - Reads from and writes to the specified `config_file_path`. This
          typically requires sudo privileges if the file is a system file.

    Raises:
        FileNotFoundError: If `config_file_path` does not exist.
        IOError: If there are issues reading from or writing to the file.
        PermissionError: If the user lacks necessary permissions for the file.
    """
    with open(config_file_path, "r") as f:
        lines = f.readlines()
    with open(config_file_path, "w") as f:
        for line in lines:
            if re.match(r"^Current=", line):
                _ = f.write(f"Current={theme_name}\n")
            else:
                _ = f.write(line)


@task_plugin(name="Setup SDDM theme", section=Sections.SYSTEM)
def setup_sddm() -> None:
    """Installs and applies a specific SDDM theme.

    This function performs the following steps:
    1. Defines the URL for a Git repository containing an SDDM theme and
       the local destination path for cloning.
    2. Defines the path to the SDDM configuration file and the theme name.
    3. Clones the SDDM theme repository into the system's SDDM themes directory
       (typically requires sudo privileges).
    4. Calls `_update_sddm_theme` to set the cloned theme as the current
       theme in the SDDM configuration file.

    Side Effects:
        - Clones a Git repository into a system directory
          (`/usr/share/sddm/themes/`), requiring sudo privileges and network access.
        - Modifies an SDDM system configuration file (`/etc/sddm.conf.d/kde_settings.conf`),
          requiring sudo privileges.
        - Logs failure messages if specific exceptions occur.

    Raises:
        TaskFailedException: If cloning the repository fails (e.g., Git not
                             found, network error, repository access issues),
                             if the SDDM configuration file is not found, or if
                             any other unexpected exception occurs during the process.
    """
    sddm_repo_name = "https://github.com/KJone1/sddm-dark-chocolate.git"
    clone_dest = "/usr/share/sddm/themes/sddm-dark-chocolate"
    sddm_config_file_path = "/etc/sddm.conf.d/kde_settings.conf"
    sddm_theme_name = "sddm-dark-chocolate"
    try:
        git_clone(repo_url=sddm_repo_name, dest=clone_dest)
        _update_sddm_theme(
            config_file_path=sddm_config_file_path, theme_name=sddm_theme_name
        )
    except ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Git clone returned a failure status code",
        )
    except AttributeError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Git not found",
        )
    except FileNotFoundError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg=f"sddm.conf configuration file not found at: {sddm_config_file_path}",
        )
    except Exception as e:
        Logger.failure(f": {e}")
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="An error occurred while installing SDDM theme",
        )
