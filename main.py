from src.software import setup_packages
from sys import stdout
from loguru import logger
from src.config import load_config

from src.utils import delete_tmp_dir


def build():
    logger.remove()
    logger.add(
        stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
    )
    load_config()
    destroy()
    logger.info("Lets Roll...")


def run():
    setup_packages()


def destroy():
    delete_tmp_dir()


if __name__ == "__main__":
    build()
    run()
    destroy()
