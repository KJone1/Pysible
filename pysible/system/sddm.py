import re
from shutil import rmtree

from sh import ErrorReturnCode

from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


class SddmTheme:

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
            Logger.failure(f"Git clone returned a failure status code -> {e}")
            success = False
        except AttributeError:
            Logger.failure("Git not found")
            success = False
        except Exception as e:
            Logger.failure(f"Failed to Clone SDDM theme -> {e}")
            success = False
        else:
            Logger.success(f"Successfully cloned {self.REPO_URL} to {self.DEST}")
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

        except FileNotFoundError:
            Logger.failure(
                f"sddm.conf configuration file not found at: {config_file_path}"
            )
        except Exception as e:
            Logger.failure(
                f"An error occurred while updating '{config_file_path}': {e}"
            )
        else:
            Logger.success(
                f"Successfully updated SDDM theme to {theme_name} in {config_file_path}"
            )
