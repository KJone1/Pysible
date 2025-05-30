import os
from collections import defaultdict

import sh
from rich.box import SIMPLE_HEAVY
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from pysible.config.settings import settings, Sections
from pysible.core.task import Task
from pysible.core.task_manager import TaskManager
from pysible.utils.log_utils import Logger
from pysible.utils.misc_utils import delete_tmp_dir


class PysibleApp:
    """
    Main application class for Pysible.

    This class is responsible for initializing the application, managing the
    user interface (displaying tasks and getting user input), and coordinating
    the execution of selected tasks.
    """
    def __init__(self):
        """
        Initializes the PysibleApp instance.

        Sets up the console, task manager, and a temporary directory for
        application use. It also clears the console screen upon initialization.

        Side Effects:
            - Deletes any existing temporary directory used by Pysible.
            - Creates a new temporary directory.
            - Clears the console screen.
        """
        self.console: Console = Console()
        self.task_manager: TaskManager = TaskManager()
        delete_tmp_dir()
        sh.mkdir("-p", settings.TMP_DIR)
        _ = os.system("clear")

    def _get_user_input(self) -> str:
        """
        Prompts the user for input and returns the stripped string.

        Displays the Pysible command prompt and waits for the user to enter
        a command or task selection.

        Returns:
            The user's input string, with leading/trailing whitespace removed.
        """
        return Prompt.ask("[bold blue]Pysible ~> [/bold blue]").strip()

    def _handle_user_input(self, choice: str):
        """
        Processes the user's input to determine which tasks to execute.

        Parses the user's choice, which can be a special command (like '00'
        for all tasks, '100' for system tasks, '200' for software tasks,
        or 'q'/'exit'/'quit' to exit) or a list of task numbers.
        Selected tasks are then executed.

        Args:
            choice: The user's input string.

        Side Effects:
            - Executes tasks based on the user's selection. Each task can have
              its own side effects (e.g., installing software, modifying files).
            - Prints informational messages or error messages to the console.
            - Exits the application if the user chooses to quit.
            - Deletes the temporary directory upon exit.
        """
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
        """
        Renders and displays a table of available tasks to the console.

        The table categorizes tasks by section (e.g., System, Software) and
        displays their assigned numbers and names. It also shows options for
        running all tasks or all tasks within a specific section.

        Side Effects:
            - Prints a formatted table to the console.
        """
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
        """
        Handles application exit by cleaning up resources.

        Currently, this involves deleting the temporary directory used by Pysible.

        Side Effects:
            - Deletes the Pysible temporary directory.
        """
        delete_tmp_dir()

    def run(self):
        """
        Starts the main application loop.

        Continuously displays the task menu, gets user input, and handles
        the input until the user chooses to exit.

        Side Effects:
            - Enters an infinite loop that can only be broken by user choosing
              to exit or by an unhandled exception.
            - Calls other methods that print to console and execute tasks.
        """
        self.console.print("[bold green]Lets Roll...[/bold green]")
        while True:
            self._render_menu_table()
            user_choice = self._get_user_input()
            self._handle_user_input(user_choice)
