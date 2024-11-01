from .dotfiles import clone_dotfiles, run_dotfiles_intall_script
from .sddm import clone_sddm_theme, update_sddm_theme
from .sudoers import setup_sudoers_for_user


def setup_system():
    """Sets up system configuration"""
    setup_sudoers_for_user()
    clone_ok = clone_sddm_theme()
    if clone_ok:
        update_sddm_theme()
    clone_ok = clone_dotfiles()
    if clone_ok:
        run_dotfiles_intall_script()
