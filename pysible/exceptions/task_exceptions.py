from typing import override


class TaskFailedException(Exception):
    def __init__(
        self,
        task_name: str,
        original_exception: Exception,
        error_msg: str | None = None,
    ):
        self.task_name: str = task_name
        self.error_msg: str | None = error_msg
        self.original_exception: Exception = original_exception
        if error_msg:
            message = f"Task '{task_name}' failed with error -> {error_msg}. Original error: {type(original_exception).__name__}: {original_exception}"
        else:
            message = f"Task '{task_name}' failed. Original error: {type(original_exception).__name__}: {original_exception}"
        super().__init__(message)

    @override
    def __str__(self):
        return f"{self.args[0]}"
