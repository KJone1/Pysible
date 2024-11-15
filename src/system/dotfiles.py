from os import path

from sh import ErrorReturnCode, bash

from src.config.constants import Consts
from src.utils.net_utils import git_clone

from src.utils.log_utils import Logger

logger = Logger()

DEST = f"{Consts.HOME_DIR}/DEV/dotfiles"


def init_dotfiles() -> None:
    clone_ok = clone_dotfiles()
    if clone_ok:
        run_dotfiles_intall_script()


def clone_dotfiles() -> bool:
    REPO_URL = "https://github.com/KJone1/dotfiles.git"
    success = True
    try:
        git_clone(repo_url=REPO_URL, dest=DEST)
    except ErrorReturnCode as e:
        logger.bad(f"Git clone returned a bad status code -> {e}")
        success = False
    except AttributeError:
        logger.bad("Git not found")
        success = False
    except Exception as e:
        logger.bad(f"Failed to Setup dotfiles -> {e}")
        success = False
    else:
        logger.good(f"Successfully cloned {REPO_URL} to {DEST}")
    return success


def run_dotfiles_intall_script() -> None:
    INSTALL_SCRIPT = path.join(DEST, "install.sh")
    try:
        bash(INSTALL_SCRIPT)
    except ErrorReturnCode as e:
        logger.bad(f"Error running dotfiles install script -> {e}")
    else:
        logger.good("dotfiles installed successfully")
