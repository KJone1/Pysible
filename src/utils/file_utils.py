import sh
from os import path, sep
from .misc_utils import sudo_run
import tarfile
import src.config.constants as const


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

    source_path = path.join(const.RESOURCES_DIR, filename)

    if not path.exists(source_path) or not path.isfile(source_path):
        raise FileNotFoundError(f"Copying {source_path} Failed -> File not found")

    try:
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
                    stripped_name = path.relpath(member.name, member.name.split(sep)[0])
                    member.name = stripped_name
                    tar.extract(member, output)
            else:
                tar.extractall(output)
    except Exception as e:
        raise e
