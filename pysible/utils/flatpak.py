from sh import flatpak, contrib
from loguru import logger
from os import getenv


def setup_flatpak_repo():
    """Add remote repo for flatpak if does not exists"""
    logger.info("Insuring flathub repo exists...")
    root_pass = getenv("ROOT_PASS")
    with contrib.sudo(password=root_pass, _with=True):
        flatpak(
            "remote-add",
            "--if-not-exists",
            "flathub",
            "https://dl.flathub.org/repo/flathub.flatpakrepo",
        )
