from sh import ErrorReturnCode

from .misc_utils import sudo_run


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
    assert package_manager in (
        "flatpak",
        "dnf",
    ), f"Unsupported package manager: {package_manager}"

    try:
        if package_manager == "dnf":
            sudo_run("dnf", "-y", "install", package)
        elif package_manager == "flatpak":
            sudo_run("flatpak", "-y", "install", "flathub", package)
    except Exception as e:
        raise e from e


def setup_flatpak_repo() -> None:
    """Add remote repo for flatpak if does not exists"""
    sudo_run(
        "flatpak",
        "remote-add",
        "--if-not-exists",
        "flathub",
        "https://dl.flathub.org/repo/flathub.flatpakrepo",
    )
