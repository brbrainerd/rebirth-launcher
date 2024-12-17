"""Custom exceptions for the Rebirth Launcher."""
from typing import Optional

class LauncherError(Exception):
    """Base exception for launcher errors."""
    def __init__(self, message: str, details: Optional[str] = None) -> None:
        self.message = message
        self.details = details
        super().__init__(message)

class GamePathError(LauncherError):
    """Raised when game path is invalid or inaccessible."""
    pass

class ModError(LauncherError):
    """Base class for mod-related errors."""
    pass

class ModInstallError(ModError):
    """Raised when mod installation fails."""
    pass

class ModUpdateError(ModError):
    """Raised when mod update fails."""
    pass

class UpdateError(ModError):
    """Raised when update operations fail."""
    pass

class VersionError(LauncherError):
    """Raised when version requirements are not met."""
    pass

class ConfigError(LauncherError):
    """Raised when configuration is invalid or inaccessible."""
    pass

class SteamError(LauncherError):
    """Raised when Steam operations fail."""
    pass 