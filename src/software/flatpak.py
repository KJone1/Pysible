from concurrent.futures import ThreadPoolExecutor
from src.utils.package_utils import install_package, setup_flatpak_repo
from loguru import logger


from yaspin import yaspin


def install_flatpak() -> None:
    """
    Installs a list of packages in parallel using flatpak.
    """
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

    logger.info(f"Starting installation of {total_packages} flatpak packages.")

    with yaspin():

        def install_flatpak_packages(package_name):
            # ThreadPoolExecutor() does not take in arguments for the function
            # so doing this hack so i can pass "dnf" as package manager
            nonlocal installed_packages
            error = install_package(package=package_name, package_manager="flatpak")
            if not error:
                installed_packages += 1
            else:
                logger.error(error)

        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(install_flatpak_packages, package_list)

    logger.info(
        f"{installed_packages}/{total_packages} flatpak packages installed successfully."
    )
