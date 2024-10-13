from sh import dnf, ErrorReturnCode, contrib, flatpak

from loguru import logger
from os import getenv


def install_package(package: str, package_manager: str = "dnf") -> bool:
    """Installs a single package using a package manager"""
    try:
        root_pass = getenv("ROOT_PASS")
        with contrib.sudo(_with=True, password=root_pass):
            if package_manager == "dnf":
                dnf("-y", "install", package)
            if package_manager == "flatpak":
                flatpak("-y", "install", "flathub", package)
            status = True
            return status
        logger.error(f"Package manager: {package_manager} is not supported")
        status = False
        return status

    except ErrorReturnCode as e:
        logger.error(
            f"Encounter an error when tried to install {package} => {e.stderr.decode('utf-8').strip()}"
        )
        status = False
        return status
