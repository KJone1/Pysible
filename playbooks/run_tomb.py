import src.software.tomb as tomb
from src.utils.log_utils import Logger
import sh


try:
    tomb.install_tomb(version="2.11")
except sh.ErrorReturnCode as e:
    error = "Encounter an ErrorReturnCode when tried to install Tomb"
    Logger.failure(f"{error} -> {e}")
except Exception as e:
    Logger.failure(f"Encounter an error when tried to install Tomb -> {e}")
