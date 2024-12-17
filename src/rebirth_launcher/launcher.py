"""Main launcher implementation for Rebirth mod pack."""
from pathlib import Path
import subprocess
import logging
from typing import Optional, Callable, Sequence

from rebirth_launcher.config import get_config, LauncherConfig
from rebirth_launcher.constants import ALLOWED_MODS
from rebirth_launcher.exceptions import (
    LauncherError,
    GamePathError,
    ModInstallError,
    ModUpdateError
)
from rebirth_launcher.update_checker import UpdateChecker, ReleaseInfo
from rebirth_launcher.steam_integration import SteamIntegration
from rebirth_launcher.archive import ArchiveHandler
from rebirth_launcher.utils import clean_directory, ensure_directory

logger = logging.getLogger(__name__)

class RebirthLauncher:
    """Main launcher class for Rebirth mod pack."""
    
    def __init__(self) -> None:
        """Initialize launcher with configuration."""
        self.config: LauncherConfig = get_config()
        self.steam: SteamIntegration = SteamIntegration()
        self.update_checker: UpdateChecker = UpdateChecker()
        self.archive_handler: ArchiveHandler = ArchiveHandler()
        
    def run(
        self,
        skip_update: bool = False,
        progress: Optional['Progress'] = None
    ) -> None:
        """Main launcher execution.
        
        Args:
            skip_update: If True, skips mod update check
            progress: Optional progress bar for update operations
        """
        try:
            logger.info("Starting Rebirth Launcher")
            
            # Verify Steam ownership
            if not self.steam.verify_ownership():
                raise LauncherError(
                    "7 Days to Die not found in Steam library",
                    "Please ensure the game is installed through Steam"
                )
            
            # Verify game installation
            if not self.config.game_path.exists():
                raise GamePathError(
                    "Game installation not found",
                    f"Expected path: {self.config.game_path}"
                )
            
            # Launch game
            self.launch_game()
            logger.info("Game launched successfully")
            
        except Exception as e:
            logger.exception("Launcher execution failed")
            raise
    
    def update(
        self,
        release_info: ReleaseInfo,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """Update mod pack to new version."""
        try:
            logger.info(f"Updating to version {release_info.tag_name}")
            
            # Clean mod directories
            if not self._clean_mod_directories():
                raise ModUpdateError(
                    "Failed to clean mod directories",
                    "Could not remove existing mods"
                )
            
            # Download and install new version
            if not self._install_mods(release_info, progress_callback):
                raise ModUpdateError(
                    "Failed to install new version",
                    "Error downloading or extracting mod files"
                )
            
            # Update configuration
            self.config.version = release_info.tag_name
            self.config.save()
            
            logger.info("Update completed successfully")
            return True
            
        except Exception as e:
            logger.exception("Update failed")
            return False
    
    def launch_game(self) -> None:
        """Launch 7 Days to Die with appropriate settings."""
        try:
            exe_path = self.config.game_path / "7DaysToDie.exe"
            
            if not exe_path.exists():
                raise GamePathError(
                    "Game executable not found",
                    f"Expected path: {exe_path}"
                )
            
            cmd = [
                str(exe_path),
                "-logfile",
                str(self.config.game_path / "output_log.txt")
            ]
            
            if self.config.disable_eac:
                cmd.append("-noeac")
            
            logger.info(f"Launching game with command: {' '.join(cmd)}")
            subprocess.Popen(cmd)
            
        except Exception as e:
            logger.exception("Failed to launch game")
            raise LauncherError("Failed to launch game", str(e))
    
    def _clean_mod_directories(self) -> bool:
        """Clean mod directories while preserving allowed mods."""
        try:
            # Clean program files mods
            if not clean_directory(self.config.mods_path, ALLOWED_MODS):
                return False
            
            # Clean appdata mods
            appdata_mods = Path(self.config.game_path).parent / "AppData" / "Mods"
            if not clean_directory(appdata_mods, ALLOWED_MODS):
                return False
            
            return True
            
        except Exception as e:
            logger.exception("Failed to clean mod directories")
            return False
    
    def _install_mods(
        self,
        release_info: ReleaseInfo,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> bool:
        """Install mods from split archives."""
        try:
            # Ensure directories exist
            ensure_directory(self.config.mods_path)
            temp_dir = Path(self.config.game_path) / "Temp"
            ensure_directory(temp_dir)
            
            # Download split archives
            if not self.update_checker.download_release_assets(
                release_info,
                temp_dir,
                progress_callback
            ):
                return False
            
            # Find downloaded split files
            split_files: Sequence[Path] = sorted(
                temp_dir.glob("*.split.*"),
                key=lambda p: int(p.suffix.split('.')[-1])
            )
            
            if not split_files:
                logger.error("No split archives found")
                return False
            
            # Extract directly from first split file
            # 7-Zip will automatically handle all parts
            if not self.archive_handler.extract_archive(
                split_files[0],  # First part contains archive info
                self.config.mods_path
            ):
                return False
            
            # Clean up split files
            for file in split_files:
                file.unlink(missing_ok=True)
            
            return True
            
        except Exception as e:
            logger.exception("Failed to install mods")
            return False 