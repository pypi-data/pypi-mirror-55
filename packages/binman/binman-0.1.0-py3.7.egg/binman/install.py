from pathlib import Path

from github import Repository

from .output import OutputManager
from .state import State


class Installer:
    def __init__(self, code_host: str, install_location: str, verbose: bool):
        self.log = OutputManager(verbose=verbose)
        self._code_host = code_host
        self._install_location = Path(install_location).expanduser()

    def _validate_and_expand_path(self, name_or_path: str) -> str:
        if not name_or_path.startswith("github.com"):  # TODO: Support multiple hosts.
            if "/" in name_or_path:
                raise ValueError("Unsupported or incomplete path")
            self.log.debug(
                f"No code host specified, assuming [{self._code_host}]"
            )  # TODO: Allow configuration of default host.
            name_or_path = f"{self._code_host}/{name_or_path}"

        return name_or_path

    def install(self, name_or_path: str, version: str) -> None:
        try:
            with State() as s:
                name_or_path = self._validate_and_expand_path(name_or_path)
                self.log.step(f"Installing from {name_or_path}@{version}")

                repo = Repository.from_url(name_or_path)
                if repo.name in s.state:
                    raise ValueError(
                        f"{repo.name} is already installed. Use `binman update` to switch versions, or `binman uninstall` to remove"
                    )
                release = repo.get_release(tag=version)
                self.log.step(release.tag_name, padding=1)
                arts = []
                for artifact in release.get_platform_assets():
                    if "md5" in artifact.download_url or "sha256" in artifact.download_url:
                        continue
                    tgt_dir = self._install_location / artifact.name
                    self.log.progress(
                        f"{artifact.name}/{artifact.platform}-{artifact.architecture} ~> {tgt_dir}", padding=2
                    )
                    artifact.download(self._install_location)
                    arts.append(tgt_dir)
                s.update_application(name=repo.name, url=name_or_path, artifacts=arts, version=release.tag_name)

                self.log.info("Installation complete")

        except Exception as e:
            self.log.error(f"{type(e).__name__}: {e}.")
            raise
