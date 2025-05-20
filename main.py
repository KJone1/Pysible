import os
from collections import defaultdict
from enum import Enum
from rich.box import SIMPLE_HEAVY
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import pysible.software.containers as containers
import pysible.modules.moonlander as moonlander
from pysible.core.app import PysibleApp
from pysible.system.sddm import SddmTheme
import pysible.utils.misc_utils as misc
from pysible.utils.log_utils import Logger

console = Console()


class Sections(Enum):
    SYSTEM = "Configure System"
    SOFTWARE = "Download and Install Software"


tasks = [
    {
        "number": "1",
        "name": "Install DNF Packages",
        "func": "dnf.py",
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "2",
        "name": "Install Flatpak Packages",
        "func": "flatpak.py",
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "3",
        "name": "Install Tomb",
        "func": "tomb.py",
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "4",
        "name": "Install Kubectl",
        "func": "kubectl.py",
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "5",
        "name": "Install Buildkit",
        "func": "buildkit.py",
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "6",
        "name": "Install Nerdctl",
        "func": containers.install_nerdctl,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "7",
        "name": "Install k9s",
        "func": "k9s.py",
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "8",
        "name": "Install k0s",
        "func": containers.install_k0s,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "9",
        "name": "Configure Dotfiles",
        "func": "dotfiles.py",
        "section": Sections.SYSTEM.value,
    },
    {
        "number": "10",
        "name": "Configure SDDM Theme",
        "func": SddmTheme,
        "section": Sections.SYSTEM.value,
    },
    {
        "number": "12",
        "name": "Configure Moonlander keyboard",
        "func": moonlander.setup_moonlander,
        "section": Sections.SYSTEM.value,
    },
]


tasks_mapping = {task["number"]: task for task in tasks}


def run_modules(selected_modules):
    for mod_number in selected_modules:
        task = tasks_mapping.get(mod_number)
        if task.get("func"):
            function = task.get("func")
            function()
        else:
            console.print(f"[!] Invalid module number: {mod_number}", style="bold red")



if __name__ == "__main__":

    app = PysibleApp()

    try:
        app.run()
    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow]Ctrl+C pressed. Exiting gracefully...[/bold yellow]"
        )
    except Exception as e:
        Logger.failure(f"An unexpected critical error occurred at the top level of Pysible: {e}")
    finally:
        try:
            app.exit_handler()
        except Exception as cleanup_err:
            Logger.failure(f"Error during final cleanup: {cleanup_err}")
            exit(1)
