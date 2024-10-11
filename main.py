from pysible.actions.packages import dnf, flatpak
from sys import stdout
from loguru import logger


def startup():
    logger.remove()
    logger.add(
        stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
    )
    logger.info("Lets Roll...")


def run():
    dnf()
    flatpak()


if __name__ == "__main__":
    startup()
    run()
