import os
import shutil
import tarfile

import sh
from loguru import logger

from src.config.constants import Consts

from .misc_utils import sudo_run


def copy_resource(filename, dest, sudo=False) -> str:
    """
    Copies a file from the 'resources' directory to a destination

    Args:
      filename: Name of the file in the 'resources' directory.
      dest: Destination path.

    Returns:
        Path of copied file.

    Raises:
      FileNotFoundError: If the file does not exist
      ErrorReturnCode: If sh.cp fails to copy
    """

    source_path = os.path.join(Consts.RESOURCES_DIR, filename)
    if not os.path.exists(source_path) or not os.path.isfile(source_path):
        raise FileNotFoundError(f"Copying {source_path} Failed -> File not found")

    try:
        destination_dir = os.path.dirname(dest)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        if sudo:
            sudo_run("cp", source_path, dest)
        else:
            sh.cp(source_path, dest)
    except sh.ErrorReturnCode as e:
        raise e from e
    else:
        return dest


def untar(input: str, output: str, strip: bool = False) -> None:
    try:
        with tarfile.open(input, "r:gz") as tar:
            if strip:
                # --strip=1
                for member in tar.getmembers():
                    stripped_name = os.path.relpath(
                        member.name, member.name.split(os.sep)[0]
                    )
                    member.name = stripped_name
                    tar.extract(member, output)
            else:
                tar.extractall(output)
    except Exception as e:
        raise e


def set_file_permissions(file_path, permission):
    """
    Sets the permissions of a file.

    Args:
        file_path: The path to the file.
        permission: The permissions to set.
    """
    try:
        sudo_run("chmod", permission, f"{file_path}")
    except ValueError as e:
        raise ValueError(
            "Error changing permissions: Invalid permission format - should be a string"
        ) from e
    except OSError as e:
        raise OSError(f"Error changing permissions of {file_path} -> {e}") from e


def copy_file(source, dest):
    """
    Copies a file from one location to another.

    Args:
      source_path: The file you want to copy.
      destination_path: where you want to copy the file.
    """
    try:
        destination_dir = os.path.dirname(dest)

        if not os.path.exists(destination_dir):
            sudo_run("mkdir", "-p", destination_dir)

        sudo_run("cp", f"{source}", f"{dest}")
    except FileNotFoundError:
        logger.error(f"Source file '{source}' not found.")
    except PermissionError:
        logger.error(f"Permission denied to copy to '{dest}'.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
