from os import path

import sh

import pysible.exceptions.dotfiles as exceptions
from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


def _run_dotfiles_install_script(dotfiles_repo_path: str) -> None:
    install_script_path = path.join(dotfiles_repo_path, "install.sh")
    bash = sh.Command("bash")
    _ = bash(install_script_path, _cwd=dotfiles_repo_path)
    Logger.info("dotfiles installed successfully")


@task_plugin(
    name="Install Dot files",
    section=Sections.SYSTEM,
)
def install_dotfiles():
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
            error_msg="Git clone returned a failure status code",
        )
    except exceptions.DotfilesInstallError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error running dotfiles install script",
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
