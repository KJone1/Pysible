from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger


class Task:
    def __init__(
        self,
        number: int,
        name: str,
        action_function,
        section: str,
        params: dict[str, str] | None = None,
    ):
        self.number: int = number
        self.name: str = name
        self.action_function = action_function
        self.section: str = section
        self.params: dict[str, str] | None = params if params is not None else {}

    def execute(self) -> None:
        try:
            self.action_function(**self.params)
            Logger.success(f"Task '{self.name}' completed successfully.")
        except Exception as e:
            raise TaskFailedException(task_name=self.name, original_exception=e) from e
