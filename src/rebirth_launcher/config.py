"""Configuration management for the Rebirth Launcher."""
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, Optional

from rebirth_launcher.constants import (
    CURRENT_GAME_VERSION,
    DEFAULT_CONFIG_FILENAME,
    DEFAULT_GAME_PATH,
    DEFAULT_MODS_PATH,
    DEFAULT_STEAM_PATH,
    MOD_HOSTING_BASE_URL,
)
from rebirth_launcher.exceptions import ConfigError, GamePathError
from rebirth_launcher.utils import is_valid_game_path

logger = logging.getLogger(__name__)

@dataclass
class LauncherConfig:
    """Configuration for the Rebirth Launcher."""
    steam_path: Path = field(default=DEFAULT_STEAM_PATH)
    game_path: Path = field(default=DEFAULT_GAME_PATH)
    mods_path: Path = field(default=DEFAULT_MODS_PATH)
    version: str = field(default=CURRENT_GAME_VERSION)
    check_updates_on_launch: bool = field(default=True)
    auto_update: bool = field(default=False)
    disable_eac: bool = field(default=True)
    custom_game_path: Optional[Path] = field(default=None)
    mod_hosting_url: str = field(default=MOD_HOSTING_BASE_URL)
    
    # Class variables
    _instance: ClassVar[Optional["LauncherConfig"]] = None
    _logger: ClassVar[logging.Logger] = logging.getLogger("LauncherConfig")
    
    def __post_init__(self) -> None:
        """Validate paths after initialization."""
        self.validate_paths()
    
    @classmethod
    def get_instance(cls) -> "LauncherConfig":
        """Get singleton instance of config."""
        if cls._instance is None:
            cls._instance = cls.load()
        return cls._instance
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "LauncherConfig":
        """Load configuration from file or create default."""
        if config_path is None:
            config_path = cls._get_default_config_path()
            
        try:
            if not config_path.exists():
                config = cls()
                config.save(config_path)
                cls._logger.info("Created new configuration file")
                return config
                
            with open(config_path, 'r') as f:
                data = json.load(f)
                
            # Convert path strings to Path objects
            for key in ['steam_path', 'game_path', 'mods_path', 'custom_game_path']:
                if key in data and data[key] is not None:
                    data[key] = Path(data[key])
                    
            config = cls(**data)
            cls._logger.info("Loaded existing configuration")
            return config
                
        except Exception as e:
            raise ConfigError("Failed to load configuration", str(e))
    
    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            config_path = self._get_default_config_path()
            
        try:
            # Convert Path objects to strings
            data = {
                k: str(v) if isinstance(v, Path) else v
                for k, v in self.__dict__.items()
                if not k.startswith('_')
            }
            
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=4)
            self._logger.info(f"Saved configuration to {config_path}")
            
        except Exception as e:
            raise ConfigError("Failed to save configuration", str(e))
    
    def validate_paths(self) -> None:
        """Validate and create necessary paths."""
        try:
            # Check custom path first
            if self.custom_game_path and is_valid_game_path(self.custom_game_path):
                self.game_path = self.custom_game_path
                self.mods_path = self.game_path / "Mods"
                return
                
            # Check default path
            if not is_valid_game_path(self.game_path):
                raise GamePathError(
                    "Game not found at configured path",
                    f"Path: {self.game_path}"
                )
                
            # Create mods directory if needed
            self.mods_path.mkdir(parents=True, exist_ok=True)
            
        except GamePathError:
            raise
        except Exception as e:
            raise ConfigError("Failed to validate paths", str(e))
    
    @staticmethod
    def _get_default_config_path() -> Path:
        """Get default configuration file path."""
        exe_path = Path(sys.executable if getattr(sys, 'frozen', False) else __file__)
        return exe_path.parent / DEFAULT_CONFIG_FILENAME

def get_config() -> LauncherConfig:
    """Get launcher configuration singleton."""
    return LauncherConfig.get_instance()