from sh import ErrorReturnCode

from utils.misc_utils import sudo_run


def install_package(package: str, package_manager: str = "dnf") -> str or None:
    """
    Installs a single package using a package manager
    Args:
      package: The package to download.
      package_manager: Which package manager to use.

    Returns:
      A tuple containing:
        - A boolean indicating success (True for OK, False for error).
        - Error or None if no error occurred.
    """
    try:
        if package_manager == "dnf":
            sudo_run("dnf", "-y", "install", package)
        if package_manager == "flatpak":
            sudo_run("flatpak", "-y", "install", "flathub", package)
        error = None
        return error

        error = f"Package manager: {package_manager} is not supported"
        return error

    except ErrorReturnCode as e:
        error = f"Encounter an error when tried to install {package} => {e.stderr.decode('utf-8').strip()}"
        return error


def setup_flatpak_repo() -> None:
    """Add remote repo for flatpak if does not exists"""
    sudo_run(
        "flatpak",
        "remote-add",
        "--if-not-exists",
        "flathub",
        "https://dl.flathub.org/repo/flathub.flatpakrepo",
    )
