class TaskFailedException(Exception):
    def __init__(self, task_name: str, original_exception: Exception):
        self.task_name = task_name
        self.original_exception = original_exception
        message = f"Task '{task_name}' failed. Original error: {type(original_exception).__name__}: {original_exception}"
        super().__init__(message)

    def __str__(self):
        return f"TaskFailedException: {self.args[0]}"
