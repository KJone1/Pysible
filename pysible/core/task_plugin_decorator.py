import functools

from pysible.config.settings import settings
from pysible.core.task import Task
from pysible.core.task_manager import Sections


def task_plugin(name: str, section: Sections, params: dict | None = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        current_task_number = len(settings.REGISTERED_TASKS) + 1
        task_instance = Task(
            number=current_task_number,
            name=name,
            action_function=wrapper,
            section=section.value,
            params=params if params else {},
        )
        settings.REGISTERED_TASKS.append(task_instance)
        return wrapper

    return decorator
