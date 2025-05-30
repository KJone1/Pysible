from os import path

import sh

from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


def _run_dotfiles_install_script(dotfiles_repo_path: str) -> None:
    """Executes the install script located in the dotfiles repository.

    Args:
        dotfiles_repo_path: The local file system path to the cloned dotfiles
                            repository.

    Side Effects:
        - Runs a shell script (`install.sh`) which can modify system
          configuration and install files.
        - Logs an informational message upon successful execution.

    Raises:
        sh.ErrorReturnCode: If the `install.sh` script exits with a non-zero
                            status code.
    """
    install_script_path = path.join(dotfiles_repo_path, "install.sh")
    bash = sh.Command("bash")
    _ = bash(install_script_path, _cwd=dotfiles_repo_path)
    Logger.info("dotfiles installed successfully")


@task_plugin(
    name="Install Dot files",
    section=Sections.SYSTEM,
)
def install_dotfiles():
    """Clones a dotfiles repository and runs its installation script.

    This function performs the following steps:
    1. Defines the target directory for the dotfiles repository and its URL.
    2. Clones the dotfiles repository from GitHub using `git_clone`.
    3. Calls `_run_dotfiles_install_script` to execute the `install.sh`
       script within the cloned repository.
    4. Logs a success message if all steps complete without error.

    Side Effects:
        - Creates a directory for the dotfiles if it doesn't exist.
        - Clones a Git repository into the specified directory.
        - Executes an external shell script which can modify user and system
          configurations.
        - Logs progress and outcome.

    Raises:
        TaskFailedException: If `git_clone` fails (e.g., network issue,
                             repository not found, git not installed), or if the
                             dotfiles installation script returns an error, or if
                             any other unexpected exception occurs.
    """
    dotfile_dir = f"{settings.HOME_DIR}/DEV/dotfiles"
    repo_url = "https://github.com/KJone1/dotfiles.git"

    try:
        git_clone(repo_url=repo_url, dest=dotfile_dir)
        _run_dotfiles_install_script(dotfiles_repo_path=dotfile_dir)
        Logger.success("Successfully setup dotfiles")

    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Dotfiles installation returned a bad status code",
        )
    except AttributeError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Git not found",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Caught unexpected dotfiles error",
        )
