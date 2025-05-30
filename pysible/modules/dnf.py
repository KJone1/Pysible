import pysible.utils.package_utils as packages
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin


@task_plugin(name="Install Core DNF Packages", section=Sections.SOFTWARE)
def install_dnf_packages():
    """Installs a predefined list of core software packages using DNF.

    This function defines a set of essential packages and uses the
    `pysible.utils.package_utils.install` utility to install them via
    the DNF package manager. The list includes a variety of tools
    such as development tools, system utilities, and applications.

    Side Effects:
        - Installs system packages using DNF. This requires sudo privileges
          and can modify the system state.
        - Logs the installation progress and results.

    Raises:
        TaskFailedException: If the `packages.install` call fails for any reason
                             (e.g., DNF not found, package not found, network issues).
                             The specific exception is caught and re-raised by the
                             `packages.install` utility.
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

    packages.install(package_manager="dnf", package_list=package_list)
