from pysible.utils.file_utils import untar
from pysible.utils.misc_utils import create_tmp_dir, sudo_run
from pysible.utils.net_utils import wget
from pysible.config.constants import Consts
from pysible.utils.log_utils import Logger


def install_tomb(version: str) -> None:
    tmp_dir_name = "tomb"
    tmp_dir_path = f"{Consts.TMP_DIR}/{tmp_dir_name}"
    url = f"https://github.com/dyne/tomb/archive/refs/tags/v{version}.tar.gz"
    file_dest = f"{tmp_dir_path}/{version}.tar.gz"

    Logger.info("Starting to install Tomb...")
    try:

        create_tmp_dir(name=tmp_dir_name)
        wget(url=url, dest=file_dest)
        untar(input=file_dest, output=tmp_dir_path, strip=True)
        sudo_run("make", "install", _cwd=tmp_dir_path, _out="/dev/null")
        Logger.success(f"Installed Tomb {version}")
    except Exception:
        raise
