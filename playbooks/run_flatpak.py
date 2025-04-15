import src.software.packages as packages
import src.utils.package_utils as pkg_utils


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
