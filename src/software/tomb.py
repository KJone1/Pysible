import sh

from src.utils.file_utils import untar
from src.utils.log_utils import Logger
from src.utils.misc_utils import create_tmp_dir, sudo_run
from src.utils.net_utils import wget

logger = Logger()


def install_tomb(version: str = "2.11") -> None:
    TMP_DIR = "tmp/tomb"

    logger.info("Starting to install Tomb...")
    try:

        create_tmp_dir(name="tomb")

        URL = f"https://github.com/dyne/tomb/archive/refs/tags/v{version}.tar.gz"
        LOCAL_FILENAME = f"{TMP_DIR}/{version}.tar.gz"
        wget(url=URL, dest=LOCAL_FILENAME)

        untar(input=LOCAL_FILENAME, output=TMP_DIR, strip=True)

        sudo_run("make", "install", _cwd=TMP_DIR, _out="/dev/null")

    except sh.ErrorReturnCode as e:
        ERROR_MSG = "Encounter an ErrorReturnCode when tried to install Tomb"
        logger.failure(f"{ERROR_MSG} -> {e}")
    except Exception as e:
        logger.failure(f"Encounter an error when tried to install Tomb -> {e}")
    else:
        logger.success(f"Installed Tomb {version}")
