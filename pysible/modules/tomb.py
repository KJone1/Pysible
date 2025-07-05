import requests
import sh

from pysible.config.settings import Sections
from pysible.core.task_plugin_decorator import task_plugin
from pysible.core.temp_directory import TempDirectory
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.file_utils import untar
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import sudo_run
from pysible.utils.net_utils import wget


@task_plugin(name="Install Tomb", section=Sections.SOFTWARE)
def install_tomb():
    api_url = "https://api.github.com/repos/dyne/tomb/tags"

    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        latest_release = response.json()[0]
        latest_version = latest_release.get("name")
        url = f"https://github.com/dyne/tomb/archive/refs/tags/{latest_version}.tar.gz"

        Logger.info(f"Starting to install Tomb {latest_version}...")

        with TempDirectory("tomb") as tmp_dir_path:
            file_dest = f"{tmp_dir_path}/{latest_version}.tar.gz"
            wget(url=url, dest=file_dest)
            untar(input_tar=file_dest, output=tmp_dir_path, strip=True)
            sudo_run("make", "install", _cwd=str(tmp_dir_path), _out="/dev/null")
            Logger.success(f"Installed Tomb {latest_version}")
    except requests.exceptions.RequestException as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Error fetching release information for tomb",
        )
    except sh.ErrorReturnCode as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Encounter an ErrorReturnCode when tried to install Tomb",
        )
    except Exception as e:
        raise TaskFailedException(
            task_name=__name__,
            original_exception=e,
            error_msg="Encounter an error when tried to install Tomb",
        )
