from sh import flatpak
from loguru import logger


def setup_flatpak_repo():
    logger.info("Insuring flathub repo exists...")
    flatpak(
        "remote-add",
        "--if-not-exists",
        "flathub",
        "https://dl.flathub.org/repo/flathub.flatpakrepo",
    )
