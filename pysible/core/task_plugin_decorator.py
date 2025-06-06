import functools

from pysible.config.settings import Sections, settings
from pysible.core.task import Task


def task_plugin(name: str, section: Sections, params: dict[str, str] | None = None):
    def decorator(func):
        current_task_number = len(settings.REGISTERED_TASKS) + 1
        task_instance = Task(
            number=current_task_number,
            name=name,
            action_function=func,
            section=section.value,
            params=params if params else {},
        )
        settings.REGISTERED_TASKS.append(task_instance)
        return func

    return decorator
