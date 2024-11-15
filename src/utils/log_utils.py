from rich.console import Console


class Logger:
    console = Console()

    def good(self, msg: str):
        self.console.print(f"[bold green] >> {msg}[/bold green]")

    def bad(self, msg: str):
        self.console.print(f"[bold red] >> {msg}[/bold red]")

    def warn(self, msg: str):
        self.console.print(f"[bold yellow] >> {msg}[/bold yellow]")
