import src.utils.package_utils as package

from src.utils.log_utils import Logger


def install(package_manager: str, package_list: set[str]) -> None:

    total_packages = len(package_list)

    Logger.info(
        f"Starting installation of {total_packages} {package_manager} packages."
    )

    try:
        installed_packages = package.install_packages_parallel(
            package_list, package_manager
        )

        Logger.info(
            f"{installed_packages}/{total_packages} {package_manager} packages installed successfully."
        )
    except AttributeError as e:
        Logger.failure(f"dnf not found {e}")
    except Exception as e:
        Logger.failure(f"Failed to download dnf packages -> {e}")
