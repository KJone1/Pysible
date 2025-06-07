import os
from collections import defaultdict

import sh
from rich.box import SIMPLE_HEAVY
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from pysible.config.settings import Sections, settings
from pysible.core.task import Task
from pysible.core.task_manager import TaskManager
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import delete_tmp_dir


class PysibleApp:
    def __init__(self):
        self.console: Console = Console()
        self.task_manager: TaskManager = TaskManager()
        delete_tmp_dir()
        sh.mkdir("-p", settings.TMP_DIR)
        _ = os.system("clear")

    def _get_user_input(self) -> str:
        return Prompt.ask("[bold blue]Pysible ~> [/bold blue]").strip()

    def _handel_user_input(self, choice: str):
        tasks_to_execute: list[Task] = []
        match choice:
            case "00":
                tasks_to_execute = self.task_manager.get_all_tasks()
                Logger.info("Selected: Run ALL tasks.")
            case "100":
                tasks_to_execute = self.task_manager.get_tasks_by_section(
                    Sections.SYSTEM
                )
                Logger.info("Selected: Run all SYSTEM tasks.")
            case "200":
                tasks_to_execute = self.task_manager.get_tasks_by_section(
                    Sections.SOFTWARE
                )
                Logger.info("Selected: Run all SOFTWARE tasks.")
            case "q" | "exit" | "quit":
                delete_tmp_dir()
                exit(0)
            case _:
                selected_modules = [
                    num.strip()
                    for num in choice.replace(",", " ").split()
                    if num.strip()
                ]
                if not selected_modules:
                    self.console.print(
                        "[bold red]Invalid Input! Please choose valid options.[/bold red]"
                    )
                for num in selected_modules:
                    task = self.task_manager.get_task(int(num))
                    if task:
                        Logger.info(f"Selected task {task.number}: {task.name}")
                        tasks_to_execute.append(task)

        for task in tasks_to_execute:
            task.execute()

    def _render_menu_table(self):
        sections = [section.value for section in Sections]
        table = Table(
            box=SIMPLE_HEAVY,
            expand=False,
            caption="[bold red]"
            + "-" * 15
            + " 00. FULL RUN "
            + "-" * 15
            + "[/bold red]",
            caption_justify="center",
        )
        table.add_column(
            Sections.SYSTEM.value, justify="full", style="green", no_wrap=True
        )
        table.add_column(
            Sections.SOFTWARE.value, justify="full", style="cyan", no_wrap=True
        )
        tasks_by_section = defaultdict(list)
        for task in self.task_manager.get_all_tasks():
            if task.section in sections:
                tasks_by_section[task.section].append(
                    f"[bold]{task.number}[/bold]. {task.name}"
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
        self.console.print(table)

    def exit_handler(self) -> None:
        delete_tmp_dir()

    def run(self):
        self.console.print("[bold green]Lets Roll...[/bold green]")
        while True:
            self._render_menu_table()
            user_choice = self._get_user_input()
            self._handel_user_input(user_choice)
