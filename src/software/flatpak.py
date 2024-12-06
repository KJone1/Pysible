from concurrent.futures import ThreadPoolExecutor

from yaspin import yaspin

from src.utils.log_utils import Logger
import src.utils.package_utils as package


def install_flatpak() -> None:
    """
    Installs a list of packages in parallel using flatpak.
    """
    package.setup_flatpak_repo()

    package_list = {
        "com.discordapp.Discord",
        "io.github.flattool.Warehouse",
        "net.nokyan.Resources",
        "md.obsidian.Obsidian",
        "io.github.zen_browser.zen",
        "com.github.tchx84.Flatseal",
    }
    total_packages = len(package_list)

    Logger.info(f"Starting installation of {total_packages} flatpak packages.")

    try:
        installed_packages = package.install_packages_parallel(package_list, "flatpak")

        Logger.info(
            f"{installed_packages}/{total_packages} flatpak packages installed successfully."
        )

    except AttributeError as e:
        Logger.failure(f"Flatpak not found {e}")
    except Exception as e:
        Logger.failure(f"Failed to download flatpak packages -> {e}")
