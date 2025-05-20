import pysible.software.containers as containers
from pysible.utils.log_utils import Logger
import sh

def install_buildkit(version:str):
    try:
        containers.install_buildkit(version)
    except sh.ErrorReturnCode as e:
        error = "Encounter an ErrorReturnCode when tried to install Tomb"
        Logger.failure(f"{error} -> {e}")
    except Exception as e:
        Logger.failure(f"Failed to install Buildkit -> {e}")
