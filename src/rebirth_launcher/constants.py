"""Constants for the Rebirth Launcher."""
from pathlib import Path
from typing import Final

# Game versions
CURRENT_GAME_VERSION: Final[str] = "1.1.0"
CURRENT_GAME_BUILD: Final[str] = "stable"

# Mod compatibility
COMPATIBLE_GAME_VERSIONS: Final[dict[str, str]] = {
    "0.1.0": "1.1.0 Stable",
    # Add future version mappings here
}

# Allowed mods (not to be removed during cleanup)
ALLOWED_MODS: Final[set[str]] = {
    "0_TFP_Harmony",  # Base game Harmony mod
}

# File paths
DEFAULT_STEAM_PATH: Final[Path] = Path(r"C:\Program Files (x86)\Steam")
DEFAULT_GAME_PATH: Final[Path] = (
    DEFAULT_STEAM_PATH / "steamapps" / "common" / "7 Days To Die"
)
DEFAULT_MODS_PATH: Final[Path] = DEFAULT_GAME_PATH / "Mods"

# Steam
STEAM_APP_ID: Final[str] = "251570"  # 7 Days to Die

# GitHub
GITHUB_REPO: Final[str] = "brbrainerd/rebirth-launcher"
GITHUB_API_BASE: Final[str] = f"https://api.github.com/repos/{GITHUB_REPO}"

# Mod hosting
MOD_HOSTING_BASE_URL: Final[str] = "https://github.com/brbrainerd/rebirth-mods/releases/download"

# Launcher settings
DEFAULT_CONFIG_FILENAME: Final[str] = "launcher_config.json"
DEFAULT_LOG_FILENAME: Final[str] = "rebirth_launcher.log"