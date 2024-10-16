from src.utils import git_clone
from loguru import logger


def setup_sddm_theme() -> None:
    REPO_URL = "https://github.com/KJone1/sddm-dark-chocolate.git"
    DEST = "/usr/share/sddm/themes/sddm-dark-chocolate"
    err = git_clone(repo_url=REPO_URL, dest=DEST)
    if err:
        logger.error(f"Failed to Setup SDDM theme with error => {err}")
        return
    logger.info(f"Successfully cloned {REPO_URL} to {DEST}")
