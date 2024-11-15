from os import path
from shutil import rmtree

import sh

from src.config.constants import Consts


def create_tmp_dir(name: str) -> None:
    sh.mkdir("-p", f"{Consts.TMP_DIR}/{name}")


def delete_tmp_dir() -> None:
    if path.exists(Consts.TMP_DIR):
        rmtree(Consts.TMP_DIR)


def sudo_run(command: str, *args, **kwargs) -> None:
    """
    executes a command with sudo privileges.
    args:
        command: the command to execute (e.g., 'make', 'ls', 'cp').
        *args:  any arguments to pass to the command.
    """
    with sh.contrib.sudo(_with=True, password=Consts.ROOT_PASS):
        getattr(sh, command)(*args, **kwargs)
