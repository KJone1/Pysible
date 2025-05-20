import pysible.software.tomb as tomb
from pysible.utils.log_utils import Logger
import sh

def install_tomb(version:str):
    try:
        tomb.install_tomb(version)
    except sh.ErrorReturnCode as e:
        error = "Encounter an ErrorReturnCode when tried to install Tomb"
        Logger.failure(f"{error} -> {e}")
    except Exception as e:
        Logger.failure(f"Encounter an error when tried to install Tomb -> {e}")
