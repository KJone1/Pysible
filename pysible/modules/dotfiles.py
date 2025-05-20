import pysible.software.dotfiles as dotfiles
import pysible.exceptions.dotfiles
import sh

from pysible.utils.log_utils import Logger
from pysible.config.settings import settings

def install_dotfiles():
    dotfile_dir = f"{settings.HOME_DIR}/DEV/dotfiles"
    repo_url = "https://github.com/KJone1/dotfiles.git"

    try:
        dotfiles.clone_dotfiles(repo_url=repo_url, dest=dotfile_dir)
        dotfiles.run_dotfiles_install_script(dotfiles_repo_path=dotfile_dir)
        Logger.success("Successfully setup dotfiles")

    except sh.ErrorReturnCode as e:
        Logger.failure(f"Git clone returned a failure status code -> {e}")
    except pysible.exceptions.dotfiles.DotfilesInstallError as e:
        Logger.failure(f"Error running dotfiles install script -> {e}")
    except AttributeError as e:
        Logger.failure(f"Git not found -> {e}")
    except Exception as e:
        Logger.failure(f"Failed to Setup dotfiles -> {e}")
