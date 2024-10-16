from sh import cp, ErrorReturnCode
import os


def copy(filename, dest) -> str or None:
    """
    Copies a file from the 'resources' directory to a destination

    Args:
      filename: Name of the file in the 'resources' directory.
      dest: Destination path.
    """
    try:
        resources_dir = os.path.join(os.path.dirname(__file__), "resources")
        source_path = os.path.join(resources_dir, filename)

        cp(source_path, dest)
        print(f"Copied {filename} to {dest}")

    except ErrorReturnCode as e:
        return f"Error copying {filename} => {e}"
    except FileNotFoundError:
        return f"Copying {source_path} Failed => File not found"
