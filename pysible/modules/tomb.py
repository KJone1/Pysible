import sh

from pysible.config.settings import Sections, settings
from pysible.core.task_plugin_decorator import task_plugin
from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.file_utils import untar
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import create_tmp_dir, sudo_run
from pysible.utils.net_utils import wget


@task_plugin(name="Install Tomb", section=Sections.SOFTWARE, params={"version": "2.11"})
def install_tomb(version: str):
    tmp_dir_name = "tomb"
    tmp_dir_path = f"{settings.TMP_DIR}/{tmp_dir_name}"
    url = f"https://github.com/dyne/tomb/archive/refs/tags/v{version}.tar.gz"
    file_dest = f"{tmp_dir_path}/{version}.tar.gz"

    Logger.info("Starting to install Tomb...")
    try:
        create_tmp_dir(name=tmp_dir_name)
        wget(url=url, dest=file_dest)
        untar(input_tar=file_dest, output=tmp_dir_path, strip=True)
        sudo_run("make", "install", _cwd=tmp_dir_path, _out="/dev/null")
        Logger.success(f"Installed Tomb {version}")
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
