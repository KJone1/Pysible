from os import getenv

from dotenv import load_dotenv
from loguru import logger


def check_exists(var: str):
    value = getenv(var)
    if value is None:
        logger.fatal(f"Missing {var} env var, Exiting...")
        exit(1)
    logger.info(f"Retrieved {value} from => '{var}'")


def load_config():
    load_dotenv()
    check_exists("ROOT_PASS")
