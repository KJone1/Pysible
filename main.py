from src.actions.packages import setup_packages
from sys import stdout
from loguru import logger
from src.utils.load_config import load_config


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


def destroy():
    pass


if __name__ == "__main__":
    build()
    run()
    destroy()
