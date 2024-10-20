import sh
from loguru import logger
from src.utils import untar, wget, create_tmp_dir
from os import getenv


def install_tomb(version: str = "2.11") -> None:
    try:
        TMP_DIR = "tmp/tomb"
        ERROR_MSG = "Encounter an error while installing Tomb, skipping..."

        logger.info("Starting to install Tomb...")
        create_tmp_dir(name="tomb")

        url = f"https://github.com/dyne/tomb/archive/refs/tags/v{version}.tar.gz"
        local_filename = f"{TMP_DIR}/{version}.tar.gz"
        err = wget(url=url, dest=local_filename)
        if err:
            logger.error(err)
            logger.error(ERROR_MSG)
            return

        err = untar(input=f"tmp/tomb/{version}.tar.gz", output=TMP_DIR, strip=True)
        if err:
            logger.error(err)
            logger.error(ERROR_MSG)
            return

        root_pass = getenv("ROOT_PASS")
        with sh.contrib.sudo(_with=True, password=root_pass):
            sh.make("install", _cwd=TMP_DIR)

        logger.info(f"Installed Tomb {version}")
    except sh.ErrorReturnCode as e:
        logger.error(
            f"Encounter an error when tried to install Tomb => {e.stderr.decode('utf-8').strip()}"
        )
