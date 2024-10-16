from .sudoers import setup_sudoers_for_user


def setup_system():
    """Sets up system configuration"""
    setup_sudoers_for_user()
