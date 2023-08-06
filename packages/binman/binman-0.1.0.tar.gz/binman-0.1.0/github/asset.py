import os
import stat
from pathlib import Path
from typing import Any, Dict

import requests


class Asset:
    def __init__(self, name: str, download_url: str, size: int) -> None:
        name, platform, architecture = name.split("-")
        self.name = name
        self.platform = platform
        self.architecture = architecture
        self.download_url = download_url

    def download(self, target_dir: Path, new_filename: str = None, executable: bool = True) -> None:
        tgt = target_dir / (new_filename or self.name)
        resp = requests.get(self.download_url)
        with open(tgt, "wb") as outfile:
            outfile.write(resp.content)

        # Make executable.
        st = os.stat(tgt)
        os.chmod(tgt, st.st_mode | stat.S_IEXEC)

    @classmethod
    def from_json(cls, asset_json: Dict[str, Any]) -> "Asset":
        return cls(name=asset_json["name"], download_url=asset_json["browser_download_url"], size=asset_json["size"])
