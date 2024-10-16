from .sudoers import setup_sudoers_for_user
from .sddm import clone_sddm_theme, update_sddm_theme


def setup_system():
    """Sets up system configuration"""
    setup_sudoers_for_user()
    clone_sddm_theme()
    update_sddm_theme()
