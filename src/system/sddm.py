import re

from sh import ErrorReturnCode

from src.utils.log_utils import Logger
from src.utils.net_utils import git_clone


class SddmTheme:

    logger = Logger()
    REPO_URL = "https://github.com/KJone1/sddm-dark-chocolate.git"
    DEST = "/usr/share/sddm/themes/sddm-dark-chocolate"

    def __init__(self) -> None:
        clone_ok = self.__clone_sddm_theme()
        if clone_ok:
            self.__update_sddm_theme()
        else:
            if path.exists(self.DEST):
                rmtree(self.DEST)

    def __clone_sddm_theme(self) -> None:
        success = True

        try:
            git_clone(repo_url=self.REPO_URL, dest=self.DEST)
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
            self.logger.success(f"Successfully cloned {self.REPO_URL} to {self.DEST}")
        return success

    def __update_sddm_theme(self) -> None:
        """Updates the SDDM theme in the KDE settings configuration file"""

        config_file_path = "/etc/sddm.conf.d/kde_settings.conf"
        theme_name = "sddm-dark-chocolate"

        try:
            with open(config_file_path, "r") as f:
                lines = f.readlines()

            with open(config_file_path, "w") as f:
                for line in lines:
                    if re.match(r"^Current=", line):
                        f.write(f"Current={theme_name}\n")
                    else:
                        f.write(line)

            self.logger.success(
                f"Successfully updated SDDM theme to {theme_name} in {config_file_path}"
            )
        except FileNotFoundError:
            self.logger.failure(
                f"sddm.conf configuration file not found at: {config_file_path}"
            )
        except Exception as e:
            self.logger.failure(
                f"An error occurred while updating '{config_file_path}': {e}"
            )
