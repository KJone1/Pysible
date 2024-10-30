from os import path
from shutil import rmtree

import sh

import src.config.constants as const


def create_tmp_dir(name: str) -> None:
    sh.mkdir("-p", f"{const.TMP_DIR}/{name}")


def delete_tmp_dir() -> None:
    if path.exists(const.TMP_DIR):
        rmtree(const.TMP_DIR)


def sudo_run(command: str, *args) -> None:
    """
    executes a command with sudo privileges.

    args:
        command: the command to execute (e.g., 'make', 'ls', 'cp').
        *args:  any arguments to pass to the command.

    raises:
        sh.ErrorReturnCode: if the command execution fails.
    """

    with sh.contrib.sudo(_with=True, password=const.ROOT_PASS):
        getattr(sh, command)(*args)
