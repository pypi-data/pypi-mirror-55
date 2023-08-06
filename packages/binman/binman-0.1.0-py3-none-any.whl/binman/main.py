import click
import sys

from typing import Dict, Any

from .config import Config
from .state import State
from .install import Installer
from .uninstall import Uninstaller
from .output import OutputManager


def do_help(exit=0) -> None:
    with click.Context(cli) as ctx:
        help = cli.get_help(ctx)
        help = help.replace(
            "  binman",
            str(click.style(" $ ", fg="green", bold=True)) + str(click.style("binman", fg="yellow", bold=True)),
        )
        click.echo(help, err=True)
        sys.exit(exit)


def get_config() -> Config:
    return Config.load()


class BinmanCLI:
    """
    Binary Application Manager.
    """

    def __init__(self, verbose: bool) -> None:
        self._verbose = verbose
        self._config = Config.load()

    def install(self, name_or_path: str, version: str = "latest") -> None:
        """
        Install an application from a github URL or purposed package name.
        """
        ins = Installer(
            code_host=self._config.default_code_host,
            install_location=self._config.install_location,
            verbose=self._verbose,
        )
        ins.install(name_or_path, version)

    def update(self, name: str, version: str = "latest") -> None:
        """
        Update an installed application. For now, this is equivalent to uninstalling & reinstalling the application.
        However, in the future, the update function will allow for strict-upgrading, explicit downgrades, etc.
        """
        url = ""
        with State() as s:
            if name in s.state:
                url = s.state[name].url

        self.uninstall(name)
        self.install(url, version=version)

    def uninstall(self, name: str) -> None:
        """
        Uninstall an application.
        """
        unins = Uninstaller(verbose=self._verbose)
        unins.uninstall(name)

    def list(self) -> None:
        """
        List installed applications.
        """
        out = OutputManager(self._verbose)
        with State() as s:
            for app in s.list_installed_applications():
                out.step(f"{app.name}@{app.version}")
                if self._verbose:
                    for art in app.artifacts:
                        out.progress(f"{art}", padding=2)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]), invoke_without_command=True)
@click.option("--verbose", "-v", default=False, is_flag=True, help="Log more information.")
@click.option("--help", "-h", default=False, is_flag=True, help="Log more information.")
@click.pass_context
def cli(ctx: click.Context, help: bool, verbose: bool):
    """binman — your friendly neighborhood bin manager"""
    if help:
        do_help(0)

    if ctx.invoked_subcommand is None:
        do_help(1)
    else:
        ctx.obj = BinmanCLI(verbose=verbose)


@cli.command()
@click.pass_obj
def list(obj: BinmanCLI) -> None:
    """
    List all installed binaries.
    """
    obj.list()


@cli.command()
@click.argument("target", type=click.STRING)
@click.argument("version", type=click.STRING, default="latest")
@click.pass_obj
def install(obj: BinmanCLI, target: str, version: str) -> None:
    """
    Install a binary from a git repository.
    """
    obj.install(name_or_path=target, version=version)


@cli.command()
@click.argument("target", type=click.STRING)
@click.pass_obj
def uninstall(obj: BinmanCLI, target: str) -> None:
    """
    Uninstalls an installed binary.
    """
    obj.uninstall(name=target)


@cli.command()
@click.argument("target", type=click.STRING)
@click.argument("version", type=click.STRING, default="latest")
@click.pass_obj
def update(obj: BinmanCLI, target: str, version: str) -> None:
    """
    Updates an installed binary.
    """
    obj.update(name=target, version=version)
