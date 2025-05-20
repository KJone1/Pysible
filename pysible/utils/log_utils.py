from rich.console import Console


class Logger:

    @staticmethod
    def log(msg: str, icon: str, color: str):
        console = Console()
        console.print(f"[{color}] {icon} {msg}[/{color}]")

    @staticmethod
    def success(msg: str):
        Logger.log(msg, icon=" ", color="bold green")

    @staticmethod
    def failure(msg: str):
        Logger.log(msg, icon="󰯆 ", color="bold red")

    @staticmethod
    def warn(msg: str):
        Logger.log(msg, icon=" ", color="bold yellow")

    @staticmethod
    def info(msg: str):
        Logger.log(msg, icon="", color="bold cyan")
