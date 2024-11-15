from concurrent.futures import ThreadPoolExecutor

from yaspin import yaspin

from src.utils.log_utils import Logger
from src.utils.package_utils import install_package, setup_flatpak_repo

logger = Logger()


def install_flatpak() -> None:
    """
    Installs a list of packages in parallel using flatpak.
    """
    try:
        setup_flatpak_repo()

        package_list = {
            "com.discordapp.Discord",
            "io.github.flattool.Warehouse",
            "net.nokyan.Resources",
            "md.obsidian.Obsidian",
            "io.github.zen_browser.zen",
            "com.github.tchx84.Flatseal",
        }
        total_packages = len(package_list)
        installed_packages = 0

        logger.good(f"Starting installation of {total_packages} flatpak packages.")

        with yaspin():

            def install_flatpak_packages(package_name):
                # ThreadPoolExecutor() does not take in arguments for the function
                # so doing this hack so i can pass "dnf" as package manager
                nonlocal installed_packages
                error = install_package(package=package_name, package_manager="flatpak")
                if not error:
                    installed_packages += 1
                else:
                    logger.bad(error)

            with ThreadPoolExecutor(max_workers=8) as executor:
                executor.map(install_flatpak_packages, package_list)

        logger.good(
            f"{installed_packages}/{total_packages} flatpak packages installed successfully."
        )
    except AttributeError as e:
        logger.bad(f"Flatpak not found {e}")
    except Exception as e:
        logger.bad(f"Failed to download flatpak packages -> {e}")
