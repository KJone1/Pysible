import os
from collections import defaultdict
from enum import Enum

from rich.box import SIMPLE_HEAVY
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

import src.software.containers as containers
import src.software.dnf as dnf
import src.software.flatpak as flatpak
import src.software.tomb as tomb
from src.system.dotfiles import Dotfiles
import src.system.moonlander as moonlander
from src.system.sddm import SddmTheme
import src.system.sudoers as sudoers
from src.config.config import load_config

# from src.system import setup_system
from src.utils.misc_utils import delete_tmp_dir

console = Console()


class Sections(Enum):
    SYSTEM = "Configure System"
    SOFTWARE = "Download and Install Software"


tasks = [
    {
        "number": "1",
        "name": "Install DNF Packages",
        "func": dnf.install_dnf,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "2",
        "name": "Install Flatpak Packages",
        "func": flatpak.install_flatpak,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "3",
        "name": "Install Tomb",
        "func": tomb.install_tomb,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "4",
        "name": "Install Kubectl",
        "func": containers.install_kubectl,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "5",
        "name": "Install Buildkit",
        "func": containers.install_buildkit,
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
        "func": containers.install_k9s,
        "section": Sections.SOFTWARE.value,
    },
    {
        "number": "8",
        "name": "Configure Dotfiles",
        "func": Dotfiles,
        "section": Sections.SYSTEM.value,
    },
    {
        "number": "9",
        "name": "Configure SDDM Theme",
        "func": SddmTheme,
        "section": Sections.SYSTEM.value,
    },
    {
        "number": "10",
        "name": "Configure Sudoers for User",
        "func": sudoers.setup_sudoers_for_user,
        "section": Sections.SYSTEM.value,
    },
    {
        "number": "11",
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


def display_table():
    sections = [section.value for section in Sections]
    table = Table(
        box=SIMPLE_HEAVY,
        expand=False,
        caption="[bold red]" + "-" * 15 + " 00. FULL RUN " + "-" * 15 + "[/bold red]",
        caption_justify="center",
    )
    table.add_column(Sections.SYSTEM.value, justify="full", style="green", no_wrap=True)
    table.add_column(
        Sections.SOFTWARE.value, justify="full", style="cyan", no_wrap=True
    )
    tasks_by_section = defaultdict(list)
    for task in tasks:
        if task.get("section") in sections:
            tasks_by_section[task.get("section")].append(
                f"[bold]{task.get("number")}[/bold]. {task.get("name")}"
            )
    max_tasks = max(len(tasks_by_section[section]) for section in sections)
    for idx in range(max_tasks):
        row = []
        for section in sections:
            if idx < len(tasks_by_section[section]):
                row.append(tasks_by_section[section][idx])
            else:
                row.append("")
        table.add_row(*row)
    table.add_row("", "", "")
    table.add_row("", "", "")
    table.add_row(
        "[bold]100[/bold]. Run All System Related Tasks",
        "[bold]200[/bold]. Run All Software Related Tasks",
    )
    console.print(table)


def main():
    load_config()
    cleanup()
    os.system("clear")
    display_table()
    console.print("[bold green]Lets Roll...[/bold green]")
    while True:
        choice = Prompt.ask("[bold blue]Pysible ~> [/bold blue]").strip()

        match choice:
            case "00":
                selected_modules = [task.get("number") for task in tasks]
                run_modules(
                    selected_modules,
                )
            case "100":
                selected_modules = [
                    task.get("number")
                    for task in tasks
                    if task("section") == Sections.SYSTEM.value
                ]
                run_modules(
                    selected_modules,
                )
            case "200":
                selected_modules = [
                    task.get("number")
                    for task in tasks
                    if task.get("section") == Sections.SOFTWARE.value
                ]
                run_modules(
                    selected_modules,
                )
            case "q" | "exit" | "quit":
                cleanup()
                exit(0)
            case _:
                selected_modules = [
                    mod.strip() for mod in choice.replace(",", " ").split()
                ]
                if all(mod in tasks_mapping for mod in selected_modules):
                    run_modules(selected_modules)
                else:
                    console.print(
                        "[bold red]Invalid Input! Please choose valid options.[/bold red]"
                    )
                    display_table()


def cleanup():
    delete_tmp_dir()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow]Ctrl+C pressed. Exiting gracefully...[/bold yellow]"
        )
        cleanup()
        exit(0)
