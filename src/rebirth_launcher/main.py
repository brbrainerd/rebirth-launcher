"""Main entry point for the Rebirth Launcher."""
import logging
import sys
from pathlib import Path
from typing import Optional

# Third-party imports
import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.prompt import Confirm

# Local imports
from rebirth_launcher.config import LauncherConfig, get_config
from rebirth_launcher.constants import DEFAULT_LOG_FILENAME
from rebirth_launcher.exceptions import LauncherError
from rebirth_launcher.launcher import RebirthLauncher
from rebirth_launcher.type_definitions import RichConsole

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DEFAULT_LOG_FILENAME),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
console = Console()
app = typer.Typer()

@app.command(name="launch")
def launch(
    skip_update: bool = typer.Option(
        False,
        "--skip-update",
        help="Skip mod update check"
    ),
) -> None:
    """Launch the game with Rebirth mod pack."""
    try:
        launcher = RebirthLauncher()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            launcher.run(
                skip_update=skip_update,
                progress=progress
            )
            
    except LauncherError as e:
        logger.error(str(e))
        if e.details:
            logger.debug(e.details)
        console.print(f"[red]Error: {e.message}[/red]")
        if e.details:
            console.print(f"[red]Details: {e.details}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Fatal error")
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

def main() -> None:
    """Entry point for the launcher."""
    app()

if __name__ == "__main__":
    main() 