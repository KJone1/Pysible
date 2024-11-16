import re

from sh import ErrorReturnCode

from src.utils.log_utils import Logger
from src.utils.net_utils import git_clone

logger = Logger()


def init_sddm() -> None:
    clone_ok = clone_sddm_theme()
    if clone_ok:
        update_sddm_theme()


def clone_sddm_theme() -> None:
    REPO_URL = "https://github.com/KJone1/sddm-dark-chocolate.git"
    DEST = "/usr/share/sddm/themes/sddm-dark-chocolate"
    success = True
    try:
        git_clone(repo_url=REPO_URL, dest=DEST)
    except ErrorReturnCode as e:
        logger.failure(f"Git clone returned a failure status code -> {e}")
        success = False
    except AttributeError:
        logger.failure("Git not found")
        success = False
    except Exception as e:
        logger.failure(f"Failed to Clone SDDM theme -> {e}")
        success = False
    else:
        logger.success(f"Successfully cloned {REPO_URL} to {DEST}")
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

        logger.success(f"Successfully updated SDDM theme to {THEME_NAME} in {CONFIG_FILE}")

    except FileNotFoundError:
        logger.failure(f"sddm.conf configuration file not found at: {CONFIG_FILE}")
    except Exception as e:
        logger.failure(f"An error occurred while updating '{CONFIG_FILE}': {e}")
