from loguru import logger
from src.utils.net_utils import git_clone
from os import path
import src.config.constants as const
from sh import bash, ErrorReturnCode

DEST = f"{const.HOME_DIR}/DEV/dotfiles"


def clone_dotfiles() -> bool:
    REPO_URL = "https://github.com/KJone1/dotfiles.git"
    success = True
    try:
        git_clone(repo_url=REPO_URL, dest=DEST)
    except ErrorReturnCode as err:
        logger.error(f"Failed to Setup dotfiles with error -> {err}")
        success = False
    else:
        logger.info(f"Successfully cloned {REPO_URL} to {DEST}")
    return success


def run_dotfiles_intall_script() -> None:
    INSTALL_SCRIPT = path.join(DEST, "install.sh")
    try:
        bash(INSTALL_SCRIPT)
    except ErrorReturnCode as e:
        logger.error(f"Error running dotfiles install script -> {e}")
    else:
        logger.info("dotfiles installed successfully")
