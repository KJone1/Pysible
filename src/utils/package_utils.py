from .misc_utils import sudo_run
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.utils.log_utils import Logger

import sh

from src.config.constants import Consts


def install_package(package: str, package_manager: str = "dnf") -> str:
    assert package_manager in (
        "flatpak",
        "dnf",
    ), f"Unsupported package manager: {package_manager}"

    if package_manager == "dnf":
        args = ["install", "-y", package]
        sudo_run("dnf", *args)
    elif package_manager == "flatpak":
        args = ["install", "-y", "flathub", package]
        sudo_run("flatpak", *args)

    return package


def install_packages_parallel(
    package_list: set[str], package_manager: str, max_workers: int = 8
) -> None:
    """
    Installs a list of packages concurrently using the specified package manager.
    """
    assert package_manager in (
        "flatpak",
        "dnf",
    ), f"Unsupported package manager: {package_manager}"
    assert len(package_list) > 0, "package list should not be empty"

    installed_packages = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                install_package, package=package, package_manager=package_manager
            )
            for package in package_list
        ]
        for future in as_completed(futures):
            if future.exception() is None:
                Logger.success(f"Installed {future.result()}")
                installed_packages += 1
            else:
                Logger.failure(f"Failed to install {future.exception().full_cmd}")
    return installed_packages


def setup_flatpak_repo() -> None:
    """Add remote repo for flatpak if does not exists"""
    sudo_run(
        "flatpak",
        "remote-add",
        "--if-not-exists",
        "flathub",
        "https://dl.flathub.org/repo/flathub.flatpakrepo",
    )
