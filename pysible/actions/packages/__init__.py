from .dnf import install_dnf
from .flatpak import install_flatpak
from .tomb import install_tomb


def setup_packages():
    """Sets up all relevant packages"""
    install_dnf()
    install_flatpak()
