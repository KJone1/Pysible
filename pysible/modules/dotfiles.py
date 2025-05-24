from os import path

import sh

import pysible.exceptions.dotfiles as exceptions
from pysible.config.settings import settings
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


def _clone_dotfiles(repo_url: str, dest: str) -> None:
    git_clone(repo_url=repo_url, dest=dest)
    Logger.info(f"Successfully cloned {repo_url} to {dest}")


def _run_dotfiles_install_script(dotfiles_repo_path: str) -> None:
    install_script_path = path.join(dotfiles_repo_path, "install.sh")
    bash = sh.Command("bash")
    try:
        _ = bash(install_script_path, _cwd=dotfiles_repo_path)
        Logger.info("dotfiles installed successfully")
    except sh.ErrorReturnCode as e:
        raise exceptions.DotfilesInstallError(
            "Failed to install dotfiles", original_exception=e
        ) from e


def install_dotfiles():
    dotfile_dir = f"{settings.HOME_DIR}/DEV/dotfiles"
    repo_url = "https://github.com/KJone1/dotfiles.git"

    try:
        _clone_dotfiles(repo_url=repo_url, dest=dotfile_dir)
        _run_dotfiles_install_script(dotfiles_repo_path=dotfile_dir)
        Logger.success("Successfully setup dotfiles")

    except sh.ErrorReturnCode as e:
        Logger.failure(f"Git clone returned a failure status code -> {e}")
    except exceptions.DotfilesInstallError as e:
        Logger.failure(f"Error running dotfiles install script -> {e}")
    except AttributeError as e:
        Logger.failure(f"Git not found -> {e}")
    except Exception as e:
        Logger.failure(f"Failed to Setup dotfiles -> {e}")
