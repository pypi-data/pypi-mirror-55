from contextlib import contextmanager
from typing import Dict, Any, ContextManager, Optional, List
from pathlib import Path

from .config import _DEFAULT_CFG_DIR

import json
import os

_STATE_PATH = _DEFAULT_CFG_DIR / "state.json"
_STATE_LOCK_PATH = _DEFAULT_CFG_DIR / "state.lock"


class LockError(Exception):
    pass


class Binary:
    name: str
    url: str
    artifacts: List[str]
    version: str

    def __init__(self, name: str, url: str, artifacts: List[str], version: str):
        self.name = name
        self.url = url
        self.artifacts = artifacts
        self.version = version

    def to_json(self) -> Dict[str, Any]:
        return {"name": self.name, "artifacts": self.artifacts, "url": self.url, "version": self.version}


class StateManager:
    def __init__(self) -> None:
        self.state: Dict[str, Binary] = self._load_state()

    def _load_state(self) -> Dict[str, Binary]:
        if _STATE_PATH.exists():
            return {name: Binary(**data) for name, data in json.loads(_STATE_PATH.read_text()).items()}
        return {}

    def save(self) -> Dict[str, Binary]:
        _STATE_PATH.write_text(json.dumps({k: v.to_json() for k, v in self.state.items()}))

    def update_application(self, name: str, url: str, artifacts: List[str], version: str) -> None:
        self.state[name] = Binary(name=name, url=url, artifacts=[str(x) for x in artifacts], version=version)

    def remove_application(self, name: str) -> None:
        if name in self.state:
            del self.state[name]

    def list_installed_applications(self) -> List[Binary]:
        return list(self.state.values())


@contextmanager
def State() -> ContextManager[StateManager]:
    if _STATE_LOCK_PATH.exists():
        raise LockError(
            "Binman is currently executing in another process. Please wait for it to complete and run this command again."
        )

    with open(_STATE_LOCK_PATH, "w") as outf:
        outf.write(str(os.getpid()))

    e: Optional[Exception] = None
    try:
        m = StateManager()
        yield m
        m.save()
    except Exception as err:
        e = err
    finally:
        _STATE_LOCK_PATH.unlink()
        if e is not None:
            raise e
