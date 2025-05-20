import sh

from pysible.utils.file_utils import copy_resource
from pysible.utils.log_utils import Logger
from pysible.config.settings import settings

def setup_sudoers():
    sudoers_file_name = f"{settings.RESOURCES_DIR}/kj"
    sudoers_path = "/etc/sudoers.d/kj"
    try:
        sh.visudo("-c", "-f", sudoers_file_name)
        _ = copy_resource(filename=sudoers_file_name, dest=sudoers_path, sudo=True)
        Logger.info(f"Copied {sudoers_file_name} to {sudoers_path}")
    except sh.ErrorReturnCode as e:
        Logger.failure(f"Error validating sudoers file: {e}")
    except FileNotFoundError as e:
        Logger.failure(f"Sudoers file not found: {e}")
