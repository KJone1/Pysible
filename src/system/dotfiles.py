from os import path

from sh import ErrorReturnCode, bash

from src.config.constants import Consts
from src.utils.log_utils import Logger
from src.utils.net_utils import git_clone
from shutil import rmtree


class Dotfiles:
    logger = Logger()
    DEST = f"{Consts.HOME_DIR}/DEV/dotfiles"
    REPO_URL = "https://github.com/KJone1/dotfiles.git"

    def __init__(self) -> None:
        clone_ok = self.__clone_dotfiles()
        if clone_ok:
            self.__run_dotfiles_intall_script()
        else:
            if path.exists(self.DEST):
                rmtree(self.DEST)

    def __clone_dotfiles(self) -> bool:
        success = True

        try:
            git_clone(repo_url=self.REPO_URL, dest=self.DEST)
        except ErrorReturnCode as e:
            self.logger.failure(f"Git clone returned a failure status code -> {e}")
            success = False
        except AttributeError:
            self.logger.failure("Git not found")
            success = False
        except Exception as e:
            self.logger.failure(f"Failed to Setup dotfiles -> {e}")
            success = False
        else:
            self.logger.success(f"Successfully cloned {REPO_URL} to {self.DEST}")
        return success

    def __run_dotfiles_intall_script(self) -> None:
        INSTALL_SCRIPT = path.join(self.DEST, "install.sh")
        try:
            bash(INSTALL_SCRIPT)
        except ErrorReturnCode as e:
            self.logger.failure(f"Error running dotfiles install script -> {e}")
        else:
            self.logger.success("dotfiles installed successfully")
