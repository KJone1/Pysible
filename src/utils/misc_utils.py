import sh
from os import path, getenv
from shutil import rmtree


ROOT_TMP_DIR = "tmp"


def create_tmp_dir(name: str) -> None:
    sh.mkdir("-p", f"{ROOT_TMP_DIR}/{name}")


def delete_tmp_dir() -> None:
    if path.exists(ROOT_TMP_DIR):
        rmtree(ROOT_TMP_DIR)


def sudo_run(command: str, *args) -> None:
    """
    executes a command with sudo privileges.

    args:
        command: the command to execute (e.g., 'make', 'ls', 'cp').
        *args:  any arguments to pass to the command.

    raises:
        sh.ErrorReturnCode: if the command execution fails.
    """
    root_pass = getenv("root_pass")
    with sh.contrib.sudo(_with=True, password=root_pass):
        getattr(sh, command)(*args)
