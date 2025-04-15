import src.software.containers as containers
from src.utils.log_utils import Logger
import sh


try:
    containers.install_buildkit(version="v0.21.0")
except sh.ErrorReturnCode as e:
    error = "Encounter an ErrorReturnCode when tried to install Tomb"
    Logger.failure(f"{error} -> {e}")
except Exception as e:
    Logger.failure(f"Failed to install Buildkit -> {e}")
