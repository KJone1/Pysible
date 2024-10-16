from sh import cp, ErrorReturnCode, contrib
from os import getenv, path
from pathlib import Path
from loguru import logger


def copy_resource(filename, dest) -> str or None:
    """
    Copies a file from the 'resources' directory to a destination

    Args:
      filename: Name of the file in the 'resources' directory.
      dest: Destination path.
    """
    try:
        root_dir = Path(__file__).absolute().parent.parent.parent
        resources_dir = path.join(root_dir, "resources")
        source_path = path.join(resources_dir, filename)

        root_pass = getenv("ROOT_PASS")
        with contrib.sudo(_with=True, password=root_pass):
            cp(source_path, dest)

        logger.info(f"Copied {filename} to {dest}")
        return None

    except ErrorReturnCode as e:
        return f"Error copying {filename} => {e}"
    except FileNotFoundError:
        return f"Copying {source_path} Failed => File not found"
