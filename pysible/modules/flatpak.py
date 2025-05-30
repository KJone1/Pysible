import pysible.utils.package_utils as packages
from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin


@task_plugin(name="Install Flatpak Packages", section=Sections.SOFTWARE)
def install_flatpak_packages():
    """Installs a predefined list of Flatpak applications.

    This function performs the following steps:
    1. Defines a set of Flatpak application IDs.
    2. Ensures the Flathub repository is set up using
       `pysible.utils.package_utils.setup_flatpak_repo`.
    3. Installs the defined Flatpak applications using
       `pysible.utils.package_utils.install` with the 'flatpak'
       package manager.

    Side Effects:
        - May add the Flathub remote repository if it's not already configured.
        - Installs Flatpak applications system-wide or user-wide, depending
          on the Flatpak setup. This requires appropriate permissions and can
          modify the system state.
        - Logs the installation progress and results.

    Raises:
        TaskFailedException: If `setup_flatpak_repo` or `packages.install`
                             fails for any reason (e.g., Flatpak not found,
                             network issues, package not found). The specific
                             exception is caught and re-raised by the utility
                             functions.
    """
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
