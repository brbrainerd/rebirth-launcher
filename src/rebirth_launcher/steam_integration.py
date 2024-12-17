"""Steam integration functionality."""
import logging
from pathlib import Path
import winreg

from rebirth_launcher.config import get_config
from rebirth_launcher.constants import STEAM_APP_ID
from rebirth_launcher.exceptions import SteamError

logger = logging.getLogger(__name__)

class SteamIntegration:
    """Handles Steam-related operations."""
    
    STEAM_REGISTRY_PATHS = [
        r"SOFTWARE\WOW6432Node\Valve\Steam",  # 64-bit Windows
        r"SOFTWARE\Valve\Steam",              # 32-bit Windows
    ]
    
    STEAM_APPS_REGISTRY_PATHS = [
        rf"SOFTWARE\WOW6432Node\Valve\Steam\Apps\{STEAM_APP_ID}",
        rf"SOFTWARE\Valve\Steam\Apps\{STEAM_APP_ID}",
        rf"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App {STEAM_APP_ID}"
    ]
    
    def __init__(self) -> None:
        """Initialize Steam integration."""
        self.config = get_config()
    
    def verify_ownership(self) -> bool:
        """Verify game ownership through Steam registry."""
        try:
            # Check Steam installation
            steam_path = self._get_steam_path()
            logger.debug(f"Steam path found: {steam_path}")
            
            # Check if game executable exists directly
            game_exe = Path(steam_path) / "steamapps" / "common" / "7 Days To Die" / "7DaysToDie.exe"
            if game_exe.exists():
                logger.info(f"Game executable found at: {game_exe}")
                return True
            
            # Fallback to registry check
            if self._is_game_owned():
                return True
                
            logger.error("Game not found in Steam registry or filesystem")
            return False
            
        except Exception as e:
            logger.exception("Steam verification failed")
            return False
    
    def _get_steam_path(self) -> Path:
        """Get Steam installation path from registry."""
        for registry_path in self.STEAM_REGISTRY_PATHS:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                    steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    logger.debug(f"Found Steam path in registry: {steam_path}")
                    return Path(steam_path)
            except Exception as e:
                logger.debug(f"Failed to read registry path {registry_path}: {e}")
                continue
                
        raise SteamError("Failed to get Steam path from registry")
    
    def _is_game_owned(self) -> bool:
        """Check if game is owned through Steam registry."""
        for registry_path in self.STEAM_APPS_REGISTRY_PATHS:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                    return bool(winreg.QueryValueEx(key, "Installed")[0])
            except Exception:
                logger.debug(f"Game not found in registry path {registry_path}")
                continue
                
        logger.debug("Game not found in Steam registry")
        return False 