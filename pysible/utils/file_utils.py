import os
import tarfile

import sh

from pysible.config.settings import settings

from .misc_utils import sudo_run


def copy_resource(filename: str, dest: str, sudo: bool = False) -> str:
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

    source_path = os.path.join(settings.RESOURCES_DIR, filename)
    if not os.path.exists(source_path) or not os.path.isfile(source_path):
        raise FileNotFoundError(f"Copying {source_path} Failed -> File not found")

    destination_dir = os.path.dirname(dest)
    if not os.path.exists(destination_dir):
        sudo_run("mkdir", "-p", destination_dir)

    if sudo:
        sudo_run("cp", source_path, dest)
    else:
        sh.cp(source_path, dest)
    return dest


def untar(input_tar: str, output: str, strip: bool = False) -> None:
    with tarfile.open(input_tar, "r:gz") as tar:
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


def set_file_permissions(file_path: str, permission: str) -> None:
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


def copy(source: str, dest: str) -> None:
    destination_dir = os.path.dirname(dest)
    if not os.path.exists(destination_dir):
        sudo_run("mkdir", "-p", destination_dir)
    sudo_run("cp", f"{source}", f"{dest}")
