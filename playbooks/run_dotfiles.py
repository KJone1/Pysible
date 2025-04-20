import src.software.dotfiles as dotfiles
import src.exceptions.dotfiles
import sh

from src.utils.log_utils import Logger
from src.config.constants import Consts

dotfile_dir = f"{Consts.HOME_DIR}/DEV/dotfiles"
repo_url = "https://github.com/KJone1/dotfiles.git"

try:
    dotfiles.clone_dotfiles(repo_url=repo_url, dest=dotfile_dir)
    dotfiles.run_dotfiles_intall_script(dotfiles_repo_path=dotfile_dir)
    Logger.success("Successfully setup dotfiles")

except sh.ErrorReturnCode as e:
    Logger.failure(f"Git clone returned a failure status code -> {e}")
except src.exceptions.dotfiles.DotfilesInstallError as e:
    Logger.failure(f"Error running dotfiles install script -> {e}")
except AttributeError as e:
    Logger.failure(f"Git not found -> {e}")
except Exception as e:
    Logger.failure(f"Failed to Setup dotfiles -> {e}")
