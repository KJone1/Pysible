from concurrent.futures import ThreadPoolExecutor, as_completed

from yaspin import yaspin

from src.utils.package_utils import install_package

from src.utils.log_utils import Logger

logger = Logger()


def install_dnf() -> None:
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
        "swaylock",
        "waybar",
        "wdisplays",
        "wlogout",
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
        "cowsay",
        "flatpak",
        "zsh",
        "make",
        "steghide",
    }
    total_packages = len(package_list)
    installed_packages = 0

    logger.info(f"Starting installation of {total_packages} dnf packages.")

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(install_package, package=package, package_manager="dnf")
            for package in package_list
        ]
        for future in as_completed(futures):
            if future.exception() is None:
                logger.success(f"Installed {future.result()}")
                installed_packages += 1
            else:
                logger.failure(f"Failed to install {future.exception().full_cmd}")
    logger.info(
        f"{installed_packages}/{total_packages} dnf packages installed successfully."
    )
