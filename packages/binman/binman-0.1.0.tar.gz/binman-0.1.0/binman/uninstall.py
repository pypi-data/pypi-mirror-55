from pathlib import Path

from .output import OutputManager
from .state import State


class Uninstaller:
    def __init__(self, verbose: bool) -> None:
        self.log = OutputManager(verbose=verbose)

    def uninstall(self, name: str) -> None:
        try:
            with State() as s:
                if name not in s.state:
                    raise ValueError(f"Application [{name}] is not installed")

                self.log.step(f"Uninstalling [{name}]")

                for artifact in s.state[name].artifacts:
                    p = Path(artifact)
                    if p.exists():
                        p.unlink()
                    self.log.progress(f"Removing {p}", padding=2)

                self.log.debug(f"Removing [{name}] from state")
                s.remove_application(name)

                self.log.info("Uninstall complete")

        except Exception as e:
            self.log.error(f"{type(e).__name__}: {e}.")
