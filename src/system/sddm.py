from src.utils.net_utils import git_clone
from loguru import logger
import re
from sh import ErrorReturnCode


def clone_sddm_theme() -> None:
    REPO_URL = "https://github.com/KJone1/sddm-dark-chocolate.git"
    DEST = "/usr/share/sddm/themes/sddm-dark-chocolate"
    success = True
    try:
        git_clone(repo_url=REPO_URL, dest=DEST)
    except ErrorReturnCode as err:
        logger.error(f"Failed to Clone SDDM theme -> {err}")
        success = False
    else:
        logger.info(f"Successfully cloned {REPO_URL} to {DEST}")
    return success


def update_sddm_theme() -> None:
    """Updates the SDDM theme in the KDE settings configuration file"""
    CONFIG_FILE = "/etc/sddm.conf.d/kde_settings.conf"
    THEME_NAME = "sddm-dark-chocolate"
    try:
        with open(CONFIG_FILE, "r") as f:
            lines = f.readlines()

        with open(CONFIG_FILE, "w") as f:
            for line in lines:
                if re.match(r"^Current=", line):
                    f.write(f"Current={THEME_NAME}\n")
                else:
                    f.write(line)

        logger.info(f"Successfully updated SDDM theme to {THEME_NAME} in {CONFIG_FILE}")

    except FileNotFoundError:
        logger.error(f"sddm.conf configuration file not found at: {CONFIG_FILE}")
    except Exception as e:
        logger.error(f"An error occurred while updating '{CONFIG_FILE}': {e}")
