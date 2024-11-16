import src.utils.file_utils as files
from src.utils.log_utils import Logger

logger = Logger()


def setup_moonlander() -> None:
    UDEV_RULES = "50-zsa.rules"
    RULES_DIR = "/etc/udev/rules.d/"
    try:
        files.copy_resource(filename=UDEV_RULES, dest=RULES_DIR)
        logger.success(f"Copied {UDEV_RULES} to {RULES_DIR}")
    except Exception as e:
        logger.failure(f"Failed to copy {UDEV_RULES} -> {e}")
