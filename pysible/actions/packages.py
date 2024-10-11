from concurrent.futures import ThreadPoolExecutor
from pysible.utils.install_package import install_package
from loguru import logger
from pysible.utils.flatpak import setup_flatpak_repo


def dnf():
    """
    Installs a list of packages using dnf in parallel.
    """

    package_list = {
        "code",
        "helm",
        "vlc",
        "solaar",
        "neovim",
        "qbittorrent",
        "wireguard-tools",
        "thunar",
        "sway",
        "waybar",
        "wl-clipboard",
        "grimshot",
        "fd-find",
        "lazygit",
        "ripgrep",
        "fzf",
        "bat",
        "stow",
        "NetworkManager-tui",
        "wofi",
        "go-task",
        "wlogout",
        "cowsay",
        "flatpak",
        "zsh",
    }
    total_packages = len(package_list)
    installed_packages = 0

    logger.info(f"Starting installation of {total_packages} dnf packages.")

    def install_dnf_packages(package_name):
        status = install_package(package=package_name, package_manager="dnf")
        return status

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(install_dnf_packages, package_list)
        for result in results:
            if result:
                installed_packages += 1
    logger.info(
        f"{installed_packages}/{total_packages} dnf packages installed successfully."
    )


def flatpak():
    """
    Installs a list of packages using flatpak in parallel.
    """
    setup_flatpak_repo()

    package_list = {
        "com.discordapp.Discord",
        "io.github.flattool.Warehouse",
        "net.nokyan.Resources",
    }
    total_packages = len(package_list)
    installed_packages = 0

    logger.info(f"Starting installation of {total_packages} flatpak packages.")

    def install_flatpak_packages(package_name):
        status = install_package(package=package_name, package_manager="flatpak")
        return status

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = executor.map(install_flatpak_packages, package_list)
        for result in results:
            if result:
                installed_packages += 1
    logger.info(
        f"{installed_packages}/{total_packages} flatpak packages installed successfully."
    )
