from rich.console import Console


class Logger:
    console = Console()

    def success(self, msg: str):
        self.console.print(f"[bold green]   {msg}[/bold green]")

    def failure(self, msg: str):
        self.console.print(f"[bold red] 󰯆  {msg}[/bold red]")

    def warn(self, msg: str):
        self.console.print(f"[bold yellow]   {msg}[/bold yellow]")

    def info(self, msg: str):
        self.console.print(f" 󱠿  {msg}", style="bold cyan")
