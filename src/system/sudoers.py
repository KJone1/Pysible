from src.utils import copy_resource
from loguru import logger
from sh import visudo, ErrorReturnCode
import src.config.constants as const


def setup_sudoers_for_user() -> None:
    SUDOERS_FILE_NAME = f"{const.RESOURCES_DIR}/kj"
    SUDOERS_PATH = "/etc/sudoers.d/kj"
    try:
        visudo("-c", "-f", SUDOERS_FILE_NAME)
        copy_resource(filename=SUDOERS_FILE_NAME, dest=SUDOERS_PATH, sudo=True)
    except ErrorReturnCode as e:
        logger.error(f"Error validating sudoers file: {e}")
    except FileNotFoundError as e:
        logger.error(e)
    else:
        logger.info(f"Copied {SUDOERS_FILE_NAME} to {SUDOERS_PATH}")
