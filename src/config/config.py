from os import getenv

import dotenv

from src.utils.log_utils import Logger

logger = Logger()


def load_env(var: str):
    v = getenv(var)
    if v is None:
        config_dict = dotenv.dotenv_values(".env")
        v = config_dict.get(var)
        if v is None:
            logger.failure(f"Missing {var} env var, Exiting...")
            exit(1)
    return v


def load_config():
    dotenv.load_dotenv()
