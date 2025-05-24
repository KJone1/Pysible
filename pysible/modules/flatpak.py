import pysible.utils.package_utils as packages
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin


@task_plugin(name="Install Flatpak Packages", section=Sections.SOFTWARE)
def install_flatpak_packages():
    package_list = {
        "com.discordapp.Discord",
        "io.github.flattool.Warehouse",
        "net.nokyan.Resources",
        "md.obsidian.Obsidian",
        "io.github.zen_browser.zen",
        "com.github.tchx84.Flatseal",
    }

    packages.setup_flatpak_repo()
    packages.install(package_manager="flatpak", package_list=package_list)
