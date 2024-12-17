"""Archive handling utilities for Rebirth Launcher."""
from pathlib import Path
import subprocess
import logging
from typing import Optional

from .exceptions import ModError
from .utils import ensure_directory

logger = logging.getLogger(__name__)

class ArchiveHandler:
    """Handles archive operations for mod files."""
    
    def __init__(self) -> None:
        """Initialize archive handler."""
        self._7zip_path = self._find_7zip()
        if not self._7zip_path:
            logger.error("7-Zip not found in common installation paths")
    
    def extract_archive(
        self,
        archive_path: Path,
        output_dir: Path,
        password: str | None = None
    ) -> bool:
        """Extract archive to specified directory."""
        try:
            if not self._7zip_path:
                raise ModError("7-Zip not found", "Please install 7-Zip")
            
            if not archive_path.exists():
                raise ModError(
                    "Archive not found",
                    f"Path: {archive_path}"
                )
            
            # Ensure output directory exists
            ensure_directory(output_dir)
            
            # Build command
            cmd = [
                str(self._7zip_path),
                "x",  # extract with full paths
                "-y",  # yes to all prompts
                f"-o{output_dir}",  # output directory
            ]
            
            if password:
                cmd.append(f"-p{password}")
            
            cmd.append(str(archive_path))
            
            # Run extraction
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                logger.error(
                    "7-Zip extraction failed: %s",
                    result.stderr
                )
                return False
            
            return True
            
        except ModError:
            raise
        except Exception as e:
            logger.exception("Failed to extract archive")
            return False
    
    def _find_7zip(self) -> Path | None:
        """Find 7-Zip executable."""
        common_paths = [
            Path(r"C:\Program Files\7-Zip\7z.exe"),
            Path(r"C:\Program Files (x86)\7-Zip\7z.exe"),
        ]
        
        for path in common_paths:
            if path.exists():
                return path
        
        return None 