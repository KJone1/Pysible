class DotfilesInstallError(Exception):
    def __init__(
        self, message="Error running dotfiles install script", original_exception=None
    ):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)

    def __str__(self):
        if self.original_exception:
            return f"{self.message}: {type(self.original_exception).__name__} - {self.original_exception}"
        return self.message
