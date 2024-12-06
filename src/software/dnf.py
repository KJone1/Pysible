import src.utils.package_utils as package

from src.utils.log_utils import Logger


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
        "kitty",
        "alacritty",
    }

    total_packages = len(package_list)

    Logger.info(f"Starting installation of {total_packages} dnf packages.")

    try:
        installed_packages = package.install_packages_parallel(package_list, "dnf")

        Logger.info(
            f"{installed_packages}/{total_packages} dnf packages installed successfully."
        )
    except AttributeError as e:
        Logger.failure(f"dnf not found {e}")
    except Exception as e:
        Logger.failure(f"Failed to download dnf packages -> {e}")
