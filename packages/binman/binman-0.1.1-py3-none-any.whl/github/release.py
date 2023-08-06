import sys
from typing import Any, Dict, List

from .asset import Asset


class Release:
    def __init__(self, tag_name: str, assets: List[Asset]) -> None:
        self.tag_name = tag_name
        self.assets = assets

    def get_platform_assets(self) -> List[Asset]:
        return [asset for asset in self.assets if asset.platform == sys.platform]

    @classmethod
    def from_json(cls, release_json: Dict[str, Any]) -> "Release":
        return cls(
            release_json["tag_name"], assets=[Asset.from_json(asst_json) for asst_json in release_json["assets"]]
        )
