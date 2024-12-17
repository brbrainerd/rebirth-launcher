"""Main entry point for the Rebirth Launcher."""
import sys
import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.prompt import Confirm

from .config import get_config, LauncherConfig
from .launcher import RebirthLauncher
from .exceptions import LauncherError
from .constants import DEFAULT_LOG_FILENAME

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

@app.command()
def launch(
    game_path: Optional[Path] = typer.Option(
        None,
        "--game-path",
        "-g",
        help="Custom game installation path"
    ),
    skip_update: bool = typer.Option(
        False,
        "--skip-update",
        "-s",
        help="Skip mod update check"
    )
) -> None:
    """Launch 7 Days to Die with Rebirth mod pack."""
    try:
        # Initialize launcher
        launcher = RebirthLauncher()
        
        # Set custom game path if provided
        if game_path:
            launcher.config.custom_game_path = game_path
        
        # Run launcher
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