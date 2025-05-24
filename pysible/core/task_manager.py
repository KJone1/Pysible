import importlib
import pkgutil

from pysible.config.settings import Sections, settings
from pysible.core.task import Task
from pysible.utils.log_utils import Logger


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self._register_tasks()

    def _load_modules(self):
        import pysible.modules

        package = pysible.modules
        for _, module_name, _ in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
        ):
            try:
                importlib.import_module(module_name)
                Logger.info(f"Discovered module: {module_name}")
            except ImportError as e:
                Logger.warn(f"Could not import module {module_name}: {e}")

    def _register_tasks(self):
        self._load_modules()

        for task in settings.REGISTERED_TASKS:
            if task.number in self.tasks:
                Logger.warn(
                    f"Task number {task.number} ('{task.name}') is duplicated from plugin system. Overwriting."
                )
            self.tasks[task.number] = task

    def get_task(self, task_number: int) -> Task | None:
        return self.tasks.get(task_number)

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def get_tasks_by_section(self, section: Sections) -> list[Task]:
        return [task for task in self.tasks.values() if task.section == section]
