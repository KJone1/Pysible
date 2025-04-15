from loguru import logger
import sh

from src.config.constants import Consts
from src.utils.file_utils import copy_resource


def setup_sudoers_for_user() -> None:
    sudoers_file_name = f"{Consts.RESOURCES_DIR}/kj"
    sudoers_path = "/etc/sudoers.d/kj"
    try:
        sh.visudo("-c", "-f", sudoers_file_name)
        _ = copy_resource(filename=sudoers_file_name, dest=sudoers_path, sudo=True)
    except sh.ErrorReturnCode as e:
        logger.error(f"Error validating sudoers file: {e}")
    except FileNotFoundError as e:
        logger.error(e)
    else:
        logger.info(f"Copied {sudoers_file_name} to {sudoers_path}")
