from typing import List

import requests

from .release import Release


class Repository:

    _RELEASES_PATTERN = "https://api.github.com/repos/{owner}/{repo}/releases"
    _LATEST_PATTERN = _RELEASES_PATTERN + "/latest"

    def __init__(self, owner: str, name: str) -> None:
        self.owner = owner
        self.name = name

    @staticmethod
    def from_url(url: str) -> "Repository":
        splitted = url.split("/")
        repo = splitted[-1]
        owner = splitted[-2]
        return Repository(owner, repo)

    def list_releases(self) -> List[Release]:
        url = Repository._RELEASES_PATTERN.format(owner=self.owner, repo=self.name)
        resp = requests.get(url)
        return [Release.from_json(rel_json) for rel_json in resp.json()]

    def get_release(self, tag: str) -> Release:
        if tag == "latest":
            url = Repository._LATEST_PATTERN.format(owner=self.owner, repo=self.name)
            resp = requests.get(url)
            return Release.from_json(resp.json())

        for r in self.list_releases():
            if r.tag_name == tag:
                return r
        raise ValueError("Release not found!")  # TODO: Custom exception.

    def __str__(self) -> str:
        return f"{self.owner}/{self.name}"

    def __repr__(self) -> str:
        return str(self)
