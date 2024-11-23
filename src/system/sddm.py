import re

from sh import ErrorReturnCode

from src.utils.log_utils import Logger
from src.utils.net_utils import git_clone


class SddmTheme:

    logger = Logger()

    def __init__(self) -> None:
        clone_ok = self.__clone_sddm_theme()
        if clone_ok:
            self.__update_sddm_theme()

    def __clone_sddm_theme(self) -> None:
        REPO_URL = "https://github.com/KJone1/sddm-dark-chocolate.git"
        DEST = "/usr/share/sddm/themes/sddm-dark-chocolate"
        success = True

        try:
            git_clone(repo_url=REPO_URL, dest=DEST)
        except ErrorReturnCode as e:
            self.logger.failure(f"Git clone returned a failure status code -> {e}")
            success = False
        except AttributeError:
            self.logger.failure("Git not found")
            success = False
        except Exception as e:
            self.logger.failure(f"Failed to Clone SDDM theme -> {e}")
            success = False
        else:
            self.logger.success(f"Successfully cloned {REPO_URL} to {DEST}")
        return success

    def __update_sddm_theme(self) -> None:
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

            self.logger.success(
                f"Successfully updated SDDM theme to {THEME_NAME} in {CONFIG_FILE}"
            )
        except FileNotFoundError:
            self.logger.failure(
                f"sddm.conf configuration file not found at: {CONFIG_FILE}"
            )
        except Exception as e:
            self.logger.failure(
                f"An error occurred while updating '{CONFIG_FILE}': {e}"
            )
