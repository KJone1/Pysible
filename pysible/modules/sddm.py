import re
from sh import ErrorReturnCode
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


def _update_sddm_theme(config_file_path:str,theme_name:str) -> None:
    """Updates the SDDM theme in the KDE settings configuration file"""
    with open(config_file_path, "r") as f:
        lines = f.readlines()
    with open(config_file_path, "w") as f:
        for line in lines:
            if re.match(r"^Current=", line):
                f.write(f"Current={theme_name}\n")
            else:
                f.write(line)

def setup_sddm() -> None:

    sddm_repo_name = "https://github.com/KJone1/sddm-dark-chocolate.git"
    clone_dest = "/usr/share/sddm/themes/sddm-dark-chocolate"
    sddm_config_file_path = "/etc/sddm.conf.d/kde_settings.conf"
    sddm_theme_name = "sddm-dark-chocolate"
    try:
        git_clone(repo_url=sddm_repo_name, dest=clone_dest)
        _update_sddm_theme(config_file_path=sddm_config_file_path, theme_name=sddm_theme_name)
    except ErrorReturnCode as e:
        Logger.failure(f"Git clone returned a failure status code -> {e}")
    except AttributeError:
        Logger.failure("Git not found")
    except FileNotFoundError:
        Logger.failure(
            f"sddm.conf configuration file not found at: {sddm_config_file_path}"
        )
    except Exception as e:
        Logger.failure(
            f"An error occurred while installing SDDM theme: {e}"
        )
