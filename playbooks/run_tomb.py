import src.software.tomb as tomb
from src.utils.log_utils import Logger
import sh


Logger.info("Starting to install Tomb...")
try:
    version: str = "2.11"
    tomb.install_tomb(version=version)
    Logger.success(f"Installed Tomb {version}")
except sh.ErrorReturnCode as e:
    error = "Encounter an ErrorReturnCode when tried to install Tomb"
    Logger.failure(f"{error} -> {e}")
except Exception as e:
    Logger.failure(f"Encounter an error when tried to install Tomb -> {e}")
