from sh import cp, ErrorReturnCode
from os import path
from pathlib import Path

from .sudo import sudo


@sudo
def copy_resource(filename, dest) -> str or None:
    """
    Copies a file from the 'resources' directory to a destination

    Args:
      filename: Name of the file in the 'resources' directory.
      dest: Destination path.

    Raises:
      FileNotFoundError: If the file does not exist
      ErrorReturnCode: If sh.cp fails to copy
    """

    ROOT_DIR = Path(__file__).absolute().parent.parent.parent
    RESOURCES_DIR = path.join(ROOT_DIR, "resources")

    source_path = path.join(RESOURCES_DIR, filename)

    if not path.exists(source_path) or not path.isfile(source_path):
        raise FileNotFoundError(f"Copying {source_path} Failed -> File not found")

    try:
        cp(source_path, dest)
    except ErrorReturnCode as e:
        raise ErrorReturnCode(f"Error copying {filename} -> {e}")
