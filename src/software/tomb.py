import sh
from loguru import logger
from src.utils.file_utils import untar
from src.utils.net_utils import wget
from src.utils.misc_utils import create_tmp_dir
from os import getenv


def install_tomb(version: str = "2.11") -> None:
    TMP_DIR = "tmp/tomb"

    logger.info("Starting to install Tomb...")
    try:

        create_tmp_dir(name="tomb")

        URL = f"https://github.com/dyne/tomb/archive/refs/tags/v{version}.tar.gz"
        LOCAL_FILENAME = f"{TMP_DIR}/{version}.tar.gz"
        wget(url=URL, dest=LOCAL_FILENAME)

        untar(input=f"tmp/tomb/{version}.tar.gz", output=TMP_DIR, strip=True)

        root_pass = getenv("ROOT_PASS")
        with sh.contrib.sudo(_with=True, password=root_pass):
            sh.make("install", _cwd=TMP_DIR)

    except sh.ErrorReturnCode as e:
        ERROR_MSG = "Encounter an ErrorReturnCode when tried to install Tomb"
        logger.error(f"{ERROR_MSG} -> {e}")
    except Exception as e:
        logger.error(f"Encounter an error when tried to install Tomb -> {e}")
    else:
        logger.info(f"Installed Tomb {version}")
