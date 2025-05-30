from pysible.exceptions.task_exceptions import TaskFailedException
from pysible.utils.log_utils import Logger


class Task:
    """
    Represents a single executable task within the Pysible application.

    Each task has a number for identification, a name, an action function
    that it performs, a section it belongs to, and optional parameters
    for the action function.
    """
    def __init__(
        self,
        number: int,
        name: str,
        action_function,
        section: str,
        params: dict[str, str] | None = None,
    ):
        """
        Initializes a Task instance.

        Args:
            number: The unique number identifying the task.
            name: The human-readable name of the task.
            action_function: The function to be executed when the task runs.
            section: The section name (e.g., "SYSTEM", "SOFTWARE") the task
                     belongs to.
            params: An optional dictionary of parameters to be passed to the
                    `action_function` when it's executed. Defaults to an
                    empty dictionary if None.
        """
        self.number: int = number
        self.name: str = name
        self.action_function = action_function
        self.section: str = section
        self.params: dict[str, str] | None = params if params is not None else {}

    def execute(self) -> None:
        """
        Executes the task's action_function with its defined parameters.

        It handles potential `TaskFailedException` raised by the action
        function and logs success or failure messages accordingly. It also
        catches any other unexpected exceptions.

        Side Effects:
            - Executes the `action_function`, which can have various side effects
              depending on its implementation (e.g., file system changes,
              network requests, command execution).
            - Logs success or failure messages to the console via `Logger`.
        """
        try:
            self.action_function(**self.params)
            Logger.success(f"Task '{self.name}' completed successfully.")
        except TaskFailedException as e:
            Logger.failure(f"{e}")
        except Exception as e:
            Logger.failure(f"This exception should have never happened: {e}")
