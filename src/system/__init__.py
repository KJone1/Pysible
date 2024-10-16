from .sudoers import setup_sudoers_for_user
from .sddm import setup_sddm_theme


def setup_system():
    """Sets up system configuration"""
    setup_sudoers_for_user()
    setup_sddm_theme()
