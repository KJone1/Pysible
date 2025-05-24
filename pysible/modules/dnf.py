import pysible.utils.package_utils as packages
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin


@task_plugin(name="Install Core DNF Packages", section=Sections.SOFTWARE)
def install_dnf_packages():
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
