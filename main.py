from pysible.actions.packages import setup_packages
from sys import stdout
from loguru import logger
from pysible.utils.load_config import load_config

from sh import rm


def build():
    logger.remove()
    logger.add(
        stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
    )
    load_config()
    logger.info("Lets Roll...")


def run():
    setup_packages()


if __name__ == "__main__":
    build()
    run()
