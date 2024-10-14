from concurrent.futures import ThreadPoolExecutor
from src.utils.install_package import install_package
from loguru import logger
from src.utils.flatpak import setup_flatpak_repo

from tqdm import tqdm


def install_flatpak():
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

    with tqdm(total=total_packages, desc="Installing...") as pbar:

        def install_flatpak_packages(package_name):
            # ThreadPoolExecutor() does not take in arguments for the function
            # so doing this hack so i can pass "dnf" as package manager
            nonlocal installed_packages
            error = install_package(package=package_name, package_manager="flatpak")
            if not error:
                installed_packages += 1
            else:
                logger.error(error)
            pbar.update(1)

        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(install_flatpak_packages, package_list)

    logger.info(
        f"{installed_packages}/{total_packages} flatpak packages installed successfully."
    )
