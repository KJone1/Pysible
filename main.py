from rich.console import Console

from pysible.core.app import PysibleApp
from pysible.utils.log_utils import Logger

console = Console()

if __name__ == "__main__":

    app = PysibleApp()

    try:
        app.run()
    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow]Ctrl+C pressed. Exiting gracefully...[/bold yellow]"
        )
    finally:
        try:
            app.exit_handler()
        except Exception as cleanup_err:
            Logger.failure(f"Error during final cleanup: {cleanup_err}")
            exit(1)
