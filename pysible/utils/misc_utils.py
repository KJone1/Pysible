import os
from shutil import rmtree

import sh

from pysible.config.settings import settings


def create_tmp_dir(name: str) -> None:
    sh.mkdir("-p", f"{settings.TMP_DIR}/{name}")


def delete_tmp_dir() -> None:
    if os.path.exists(settings.TMP_DIR):
        rmtree(settings.TMP_DIR)


def sudo_run(command: str, *args: str, **kwargs: str) -> None:
    """
    executes a command with sudo privileges.
    args:
        command: the command to execute (e.g., 'make', 'ls', 'cp').
        *args:  any arguments to pass to the command.
    """
    with sh.contrib.sudo(_with=True, password=settings.ROOT_PASS):
        getattr(sh, command)(*args, **kwargs)
