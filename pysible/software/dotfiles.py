from os import path
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone
import pysible.exceptions.dotfiles as exceptions
import sh


def clone_dotfiles(repo_url: str, dest: str) -> None:
    git_clone(repo_url=repo_url, dest=dest)
    Logger.info(f"Successfully cloned {repo_url} to {dest}")


def run_dotfiles_install_script(dotfiles_repo_path: str) -> None:
    install_script_path = path.join(dotfiles_repo_path, "install.sh")
    bash = sh.Command("bash")
    try:
        _ = bash(install_script_path, _cwd=dotfiles_repo_path)
        Logger.info("dotfiles installed successfully")
    except sh.ErrorReturnCode as e:
        raise exceptions.DotfilesInstallError(
            "Failed to install dotfiles", original_exception=e
        ) from e
