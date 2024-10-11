from sh import dnf, ErrorReturnCode, contrib, flatpak
from .load_config import load_config

from loguru import logger

root_pass = load_config()["ROOT_PASS"]


def install_package(package: str, package_manager: str = "dnf") -> bool:
    """Installs a single package using a package manager"""
    try:
        with contrib.sudo(password=root_pass, _with=True):
            if package_manager == "dnf":
                dnf("-y", "install", package)
            if package_manager == "flatpak":
                flatpak("-y", "install", package)
            status = True
            return status
        logger.error(f"Package manager: {package_manager} is not supported")
        status = False
        return status

    except ErrorReturnCode as e:
        logger.error(
            f"Encounter an error when tried to install {package} => {e.stderr}"
        )
        status = False
        return status
