import importlib
import pkgutil

from pysible.config.settings import Sections, settings
from pysible.core.task import Task
from pysible.utils.log_utils import Logger


class TaskManager:
    """
    Manages the discovery, registration, and retrieval of tasks.

    This class is responsible for loading task modules, registering tasks
    that are decorated with `@task_plugin`, and providing methods to access
    these tasks by number, section, or to get all available tasks.
    """
    def __init__(self):
        """
        Initializes the TaskManager instance.

        It creates an empty dictionary to store tasks and then calls
        `_register_tasks` to discover and load all available tasks from
        the `pysible.modules` package.
        """
        self.tasks: dict[int, Task] = {}
        self._register_tasks()

    def _load_modules(self):
        """
        Dynamically imports all modules within the `pysible.modules` package.

        This is a prerequisite for task registration, as tasks are typically
        defined within these modules and registered upon module import via
        decorators.

        Side Effects:
            - Imports Python modules. This can lead to execution of code at the
              module level within each imported module.
            - Logs a warning if a module cannot be imported.
        """
        import pysible.modules

        package = pysible.modules
        for _, module_name, _ in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
        ):
            try:
                _ = importlib.import_module(module_name)
            except ImportError as e:
                Logger.warn(f"Could not import module {module_name}: {e}")

    def _register_tasks(self):
        """
        Registers tasks found in the application settings.

        This method first ensures all modules are loaded by calling `_load_modules`.
        It then iterates through tasks stored in `settings.REGISTERED_TASKS`
        (which are populated by the `@task_plugin` decorator during module import)
        and adds them to the `self.tasks` dictionary.

        Side Effects:
            - Populates the `self.tasks` dictionary.
            - Logs a warning if a task number is duplicated, overwriting the
              previous task with the new one.
        """
        self._load_modules()

        for task in settings.REGISTERED_TASKS:
            if task.number in self.tasks:
                Logger.warn(
                    f"Task number {task.number} ('{task.name}') is duplicated from plugin system. Overwriting."
                )
            self.tasks[task.number] = task

    def get_task(self, task_number: int) -> Task | None:
        """
        Retrieves a specific task by its number.

        Args:
            task_number: The unique number of the task to retrieve.

        Returns:
            The `Task` object if found, otherwise `None`.
        """
        return self.tasks.get(task_number)

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieves a list of all registered tasks.

        Returns:
            A list containing all `Task` objects, sorted by task number
            (due to dict insertion order in modern Python, but not guaranteed
            for older versions).
        """
        return list(self.tasks.values())

    def get_tasks_by_section(self, section: Sections) -> list[Task]:
        """
        Retrieves a list of tasks belonging to a specific section.

        Args:
            section: An enum member of `pysible.config.settings.Sections`
                     representing the section to filter by (e.g., Sections.SYSTEM).

        Returns:
            A list of `Task` objects that belong to the specified section.
        """
        return [task for task in self.tasks.values() if task.section == section.value]
