import pysible.software.containers as containers
from pysible.utils.log_utils import Logger
import sh

try:
    containers.install_k9s(version="v0.50.3")

except (OSError, ValueError) as e:
    Logger.failure(f"Failed to set k9s permissions -> {e}")
except sh.ErrorReturnCode as e:
    Logger.failure(f"DNF[{e.exit_code}] install failed -> {e.stderr}")
except sh.CommandNotFound as e:
    Logger.failure(
        f"Error: Command 'dnf' not found. Is dnf installed and in the system PATH?",
    )
except Exception as e:
    Logger.failure(f"Caught unexpected k9s error -> {e}")
