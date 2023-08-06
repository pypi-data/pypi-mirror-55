import json
from pathlib import Path
from typing import Any, Dict

_DEFAULT_CFG_DIR = Path("~").expanduser() / ".config" / "purposed" / "binman"
_DEFAULT_CFG_DIR.mkdir(exist_ok=True, parents=True)
_DEFAULT_CFG_PATH = _DEFAULT_CFG_DIR / "config.json"


class Config:
    default_code_host: str = "github.com/purposed"
    install_location: str = "~/bin"

    @staticmethod
    def load() -> "Config":
        if _DEFAULT_CFG_PATH.exists():
            return Config(**json.loads(_DEFAULT_CFG_PATH.read_text()))

        # Fallback on default settings.
        return Config()
