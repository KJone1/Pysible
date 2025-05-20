import pysible.system.sudoers as sudoers
import sh
from pysible.utils.log_utils import Logger
from pysible.config.settings import settings

def setup_sudoers():
    sudoers_file_name = f"{settings.RESOURCES_DIR}/kj"
    sudoers_path = "/etc/sudoers.d/kj"
    try:
        sudoers.setup_sudoers_for_user(sudoers_file_name, sudoers_path)
        Logger.info(f"Copied {sudoers_file_name} to {sudoers_path}")
    except sh.ErrorReturnCode as e:
        Logger.failure(f"Error validating sudoers file: {e}")
    except FileNotFoundError as e:
        Logger.failure(f"Sudoers file not found: {e}")
