from sh import dnf, ErrorReturnCode, contrib, flatpak

from os import getenv


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
    root_pass = getenv("ROOT_PASS")
    try:
        with contrib.sudo(_with=True, password=root_pass):
            if package_manager == "dnf":
                dnf("-y", "install", package)
            if package_manager == "flatpak":
                flatpak("-y", "install", "flathub", package)
            error = None
            return error

        error = f"Package manager: {package_manager} is not supported"
        return error

    except ErrorReturnCode as e:
        error = f"Encounter an error when tried to install {package} => {e.stderr.decode('utf-8').strip()}"
        return error
