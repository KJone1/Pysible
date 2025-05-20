import os
import subprocess
import sys

from shutil import rmtree

import sh

from pysible.config.settings import settings


def create_tmp_dir(name: str) -> None:
    sh.mkdir("-p", f"{settings.TMP_DIR}/{name}")


def delete_tmp_dir() -> None:
    if os.path.exists(settings.TMP_DIR):
        rmtree(settings.TMP_DIR)


def sudo_run(command: str, *args, **kwargs) -> None:
    """
    executes a command with sudo privileges.
    args:
        command: the command to execute (e.g., 'make', 'ls', 'cp').
        *args:  any arguments to pass to the command.
    """
    with sh.contrib.sudo(_with=True, password=settings.ROOT_PASS):
        getattr(sh, command)(*args, **kwargs)


def execute_playbook(playbook_filename: str):
    """
    Executes the specified Python playbook file using subprocess.

    Args:
        playbook_filename (str): The path to the Python script to execute.

    Returns:
        bool: True if execution was successful (exit code 0), False otherwise.
    """
    playbook_filename = os.path.join("playbooks", playbook_filename)

    if not os.path.exists(playbook_filename):
        print(f"Error: Playbook file '{playbook_filename}' not found.")
        return False

    project_root = settings.ROOT_DIR

    new_env = os.environ.copy()

    current_pythonpath = new_env.get("PYTHONPATH", "")
    new_env["PYTHONPATH"] = f"{project_root}{os.pathsep}{current_pythonpath}".rstrip(
        os.pathsep
    )

    try:
        _ = subprocess.run(
            [sys.executable, playbook_filename], check=True, text=True, env=new_env
        )
        return True
    except FileNotFoundError:
        # This might happen if sys.executable is somehow invalid,
        # though the os.path.exists check handles the script file itself.
        print(f"Error: Python interpreter '{sys.executable}' not found.")
        return False
    except subprocess.CalledProcessError as e:
        # The playbook script exited with an error (non-zero exit code)
        print(
            f"Error: Playbook '{playbook_filename}' failed with exit code {e.returncode}."
        )
        # e.stdout and e.stderr might contain captured output if capture_output=True
        return False
    except Exception as e:
        # Catch any other unexpected errors during execution attempt
        print(
            f"An unexpected error occurred while trying to run '{playbook_filename}': {e}"
        )
        return False
