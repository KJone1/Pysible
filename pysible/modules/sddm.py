import re

from sh import ErrorReturnCode

from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger
from pysible.utils.net_utils import git_clone


def _update_sddm_theme(config_file_path: str, theme_name: str) -> None:
    """Updates the SDDM theme in the KDE settings configuration file"""
    with open(config_file_path, "r") as f:
        lines = f.readlines()
    with open(config_file_path, "w") as f:
        for line in lines:
            if re.match(r"^Current=", line):
                _ = f.write(f"Current={theme_name}\n")
            else:
                _ = f.write(line)


@task_plugin(name="Setup SDDM theme", section=Sections.SYSTEM)
def setup_sddm() -> None:

    sddm_repo_name = "https://github.com/KJone1/sddm-dark-chocolate.git"
    clone_dest = "/usr/share/sddm/themes/sddm-dark-chocolate"
    sddm_config_file_path = "/etc/sddm.conf.d/kde_settings.conf"
    sddm_theme_name = "sddm-dark-chocolate"
    try:
        git_clone(repo_url=sddm_repo_name, dest=clone_dest)
        _update_sddm_theme(
            config_file_path=sddm_config_file_path, theme_name=sddm_theme_name
        )
    except ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Git clone returned a failure status code",
        )
    except AttributeError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Git not found",
        )
    except FileNotFoundError as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg=f"sddm.conf configuration file not found at: {sddm_config_file_path}",
        )
    except Exception as e:
        Logger.failure(f": {e}")
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="An error occurred while installing SDDM theme",
        )
