from enum import Enum

from pysible.core.task import Task
from pysible.modules.dnf import install_dnf_packages
from pysible.modules.flatpak import install_flatpak_packages
from pysible.modules.buildkit import install_buildkit
from pysible.modules.dotfiles import install_dotfiles
from pysible.modules.k9s import install_k9s
from pysible.modules.kubectl import install_kubectl
from pysible.modules.tomb import install_tomb
from pysible.utils.log_utils import Logger


class Sections(Enum):
    SYSTEM = "Configure System"
    SOFTWARE = "Download and Install Software"


class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self._register_tasks()

    def _register_tasks(self):

        task_definitions = [
            Task(
                number=1,
                name="Install Core DNF Packages",
                action_function=install_dnf_packages,
                section=Sections.SOFTWARE.value,
            ),
            Task(
                number=2,
                name="Install Flatpak Packages",
                action_function=install_flatpak_packages,
                section=Sections.SOFTWARE.value,
            ),
            Task(
                number=3,
                name="Install Tomb",
                action_function=install_tomb,
                section=Sections.SOFTWARE.value,
                params={"version":"2.11"}
            ),
            Task(
                number=4,
                name="Install Dot files",
                action_function=install_dotfiles,
                section=Sections.SYSTEM.value,
            ),
            Task(
                number=5,
                name="Install Kubectl",
                action_function="kubectl.py",
                section=Sections.SOFTWARE.value,
            ),
            Task(
                number=6,
                name="Install Buildkit",
                action_function=install_buildkit,
                section=Sections.SOFTWARE.value,
                params={"version":"v0.21.0"}
            ),
            Task(
                number=6,
                name="Install k9s",
                action_function=install_k9s,
                section=Sections.SOFTWARE.value,
                params={"version": "v0.50.3"}
            ),
            Task(
                number=6,
                name="Install kubectl",
                action_function=install_kubectl,
                section=Sections.SOFTWARE.value,
            ),


        ]
        for task in task_definitions:
            if task.number in self.tasks:
                Logger.warn(
                    f"Task number {task.number} ('{task.name}') is duplicated. Overwriting."
                )
            self.tasks[task.number] = task

    def get_task(self, task_number: int) -> Task | None:
        return self.tasks.get(task_number)

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def get_tasks_by_section(self, section: Sections) -> list[Task]:
        return [task for task in self.tasks.values() if task.section == section]
