from concurrent.futures import ThreadPoolExecutor
from src.utils.install_package import install_package
from loguru import logger
from tqdm import tqdm


def install_dnf():
    """
    Installs a list of packages in parallel using dnf.
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

    with tqdm(total=total_packages, desc="Installing...") as pbar:

        def install_dnf_packages(package_name):
            # ThreadPoolExecutor() does not take in arguments for the function
            # so doing this hack so i can pass "dnf" as package manager
            nonlocal installed_packages
            error = install_package(package=package_name, package_manager="dnf")
            if not error:
                installed_packages += 1
            else:
                logger.error(error)
            pbar.update(1)

        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(install_dnf_packages, package_list)

    logger.info(
        f"{installed_packages}/{total_packages} dnf packages installed successfully."
    )
