from sh import mkdir

from os import path
from shutil import rmtree


ROOT_TMP_DIR = "tmp"


def create_tmp_dir(name: str) -> None:
    mkdir("-p", f"{ROOT_TMP_DIR}/{name}")


def delete_tmp_dir() -> None:
    if path.exists(ROOT_TMP_DIR):
        rmtree(ROOT_TMP_DIR)
