import pysible.utils.package_utils as package

from pysible.utils.log_utils import Logger


def install(package_manager: str, package_list: set[str]) -> None:

    package_count = len(package_list)

    Logger.info(f"Starting installation of {package_count} {package_manager} packages.")

    try:
        installed_packages = package.install_packages_parallel(
            package_list, package_manager
        )

        Logger.info(
            f"{installed_packages}/{package_count} {package_manager} packages installed successfully."
        )
    except AttributeError as e:
        Logger.failure(f"{package_manager} not found {e}")
    except Exception as e:
        Logger.failure(f"Failed to download {package_manager} packages -> {e}")
