import pysible.utils.package_utils as packages
import pysible.utils.package_utils as pkg_utils


def install_flatpak_packages():
    package_list = {
        "com.discordapp.Discord",
        "io.github.flattool.Warehouse",
        "net.nokyan.Resources",
        "md.obsidian.Obsidian",
        "io.github.zen_browser.zen",
        "com.github.tchx84.Flatseal",
    }

    pkg_utils.setup_flatpak_repo()

    packages.install(package_manager="flatpak", package_list=package_list)
