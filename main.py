from rich.console import Console

from pysible.core.app import PysibleApp

console = Console()

if __name__ == "__main__":

    app = PysibleApp()

    try:
        app.run()
    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow]Ctrl+C pressed. Exiting gracefully...[/bold yellow]"
        )
