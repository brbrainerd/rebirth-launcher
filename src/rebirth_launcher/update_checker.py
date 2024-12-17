"""Update checking and downloading functionality."""
from dataclasses import dataclass
from pathlib import Path
import logging
from typing import Callable

import requests

from rebirth_launcher.config import get_config
from rebirth_launcher.constants import GITHUB_API_BASE
from rebirth_launcher.exceptions import LauncherError

logger = logging.getLogger(__name__)

@dataclass
class ReleaseInfo:
    """Information about a mod release."""
    version: str
    chunks: list[str]
    checksum: str
    changelog: str | None = None

class UpdateChecker:
    """Checks for and downloads mod updates."""
    
    def __init__(self) -> None:
        """Initialize update checker."""
        self.config = get_config()
        self.session = requests.Session()
    
    def download_release_assets(
        self,
        release_info: ReleaseInfo,
        output_dir: Path,
        progress_callback: Callable[[float], None] | None = None
    ) -> bool:
        """Download release assets from external hosting."""
        try:
            base_url = self.config.mod_hosting_url
            version = release_info.version
            
            # Download split files
            for chunk_name in release_info.chunks:
                url = f"{base_url}/v{version}/{chunk_name}"
                output_path = output_dir / chunk_name
                
                self._download_file(url, output_path, progress_callback)
            
            return True
            
        except Exception:
            logger.exception("Failed to download assets")
            return False
    
    def _download_file(
        self,
        url: str,
        output_path: Path,
        progress_callback: Callable[[float], None] | None = None,
        chunk_size: int = 8192
    ) -> None:
        """Download a file with progress tracking."""
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()
            
            total = int(response.headers.get('content-length', 0))
            
            with open(output_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback and total:
                        progress_callback(downloaded / total)
                        
        except Exception as e:
            raise LauncherError(
                "Failed to download file",
                f"URL: {url}, Error: {str(e)}"
            )