from loguru import logger
import sh

from pysible.config.settings import settings
from pysible.utils.file_utils import copy_resource


def setup_sudoers_for_user(sudoers_file_name: str, sudoers_path: str) -> None:
    sh.visudo("-c", "-f", sudoers_file_name)
    _ = copy_resource(filename=sudoers_file_name, dest=sudoers_path, sudo=True)
