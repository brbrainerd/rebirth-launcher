"""Utility functions for the Rebirth Launcher."""
from collections.abc import Iterator
from pathlib import Path
import hashlib
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def calculate_checksum(file_path: Path, chunk_size: int = 8192) -> str | None:
    """Calculate SHA256 checksum of a file."""
    try:
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        logger.exception(f"Error calculating checksum for {file_path}")
        return None

def ensure_directory(path: Path) -> bool:
    """Ensure directory exists, create if necessary."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        logger.exception(f"Error creating directory {path}")
        return False

def clean_directory(path: Path, preserve: set[str] | None = None) -> bool:
    """Clean directory contents, optionally preserving specified items."""
    try:
        if not path.exists():
            return True

        preserve = preserve or set()
        for item in path.iterdir():
            if item.name in preserve:
                continue
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                clean_directory(item)
                item.rmdir()
        return True
    except Exception:
        logger.exception(f"Error cleaning directory {path}")
        return False

def is_valid_game_path(path: Path) -> bool:
    """Check if path contains valid 7 Days to Die installation."""
    try:
        exe_path = path / "7DaysToDie.exe"
        return exe_path.is_file()
    except Exception:
        logger.exception(f"Error checking game path {path}")
        return False 