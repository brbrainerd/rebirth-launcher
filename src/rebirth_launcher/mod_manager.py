"""Mod management functionality for Rebirth Launcher."""
from pathlib import Path
import json
import logging
from dataclasses import dataclass
from typing import Callable

import requests

from rebirth_launcher.config import get_config
from rebirth_launcher.exceptions import ModError
from rebirth_launcher.utils import ensure_directory, clean_directory

logger = logging.getLogger(__name__)

@dataclass
class ModInfo:
    """Information about a mod."""
    name: str
    version: str
    description: str | None = None
    author: str | None = None
    dependencies: list[str] | None = None

class ModManager:
    """Manages mod installation and updates."""
    
    def __init__(self, config: LauncherConfig) -> None:
        """Initialize mod manager with configuration."""
        self.config = config
        self.session = requests.Session()
    
    def install_mod(
        self,
        mod_info: ModInfo,
        progress_callback: Callable[[float], None] | None = None
    ) -> bool:
        """
        Install or update a mod.
        
        Args:
            mod_info: Information about the mod to install
            progress_callback: Optional callback for installation progress
            
        Returns:
            bool: True if installation successful, False otherwise
            
        Raises:
            ModError: If installation fails
        """
        try:
            # Ensure mod directory exists
            if not ensure_directory(self.config.mods_path):
                raise ModError(
                    f"Failed to create mod directory: {self.config.mods_path}"
                )
            
            # Clean existing mod files if updating
            mod_path = self.config.mods_path / mod_info.name
            if mod_path.exists():
                if not clean_directory(mod_path):
                    raise ModError(
                        f"Failed to clean existing mod directory: {mod_path}"
                    )
            
            # Download mod files
            url = f"{self.config.mod_hosting_url}/mods/{mod_info.name}/v{mod_info.version}"
            try:
                response = self.session.get(url, stream=True)
                response.raise_for_status()
            except requests.RequestException as e:
                raise ModError(
                    f"Failed to download mod {mod_info.name}",
                    f"URL: {url}, Error: {str(e)}"
                )
            
            total = int(response.headers.get('content-length', 0))
            
            try:
                with open(mod_path, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total:
                            progress_callback(downloaded / total)
            except IOError as e:
                raise ModError(
                    f"Failed to write mod file: {mod_path}",
                    str(e)
                )
            
            return True
            
        except ModError:
            raise
        except Exception as e:
            logger.exception("Unexpected error during mod installation")
            raise ModError(
                f"Failed to install mod {mod_info.name}",
                str(e)
            )