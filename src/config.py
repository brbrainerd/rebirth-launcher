from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json
import sys

@dataclass
class LauncherConfig:
    steam_path: Path = Path(r"C:\Program Files (x86)\Steam")
    game_path: Path = steam_path / "steamapps" / "common" / "7 Days To Die"
    mods_path: Path = game_path / "Mods"
    repo_url: str = "https://github.com/your-org/rebirth-modpack"
    check_updates_on_launch: bool = True
    auto_update: bool = True
    disable_eac: bool = True
    
    @classmethod
    def load(cls, config_path: Path) -> "LauncherConfig":
        if not config_path.exists():
            config = cls()
            config.save(config_path)
            return config
            
        with open(config_path, 'r') as f:
            data = json.load(f)
            return cls(**{k: Path(v) if k.endswith('_path') else v 
                        for k, v in data.items()})
    
    def save(self, config_path: Path) -> None:
        data = {k: str(v) if isinstance(v, Path) else v 
                for k, v in self.__dict__.items()}
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=4)

def get_config() -> LauncherConfig:
    exe_path = Path(sys.executable if getattr(sys, 'frozen', False) else __file__)
    config_path = exe_path.parent / "launcher_config.json"
    return LauncherConfig.load(config_path)