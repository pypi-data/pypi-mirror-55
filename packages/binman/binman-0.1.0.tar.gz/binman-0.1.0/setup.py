from setuptools import find_packages, setup

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip


def get_version():
    with open("VERSION.txt") as f:
        version = f.read().strip()

    if not version:
        raise RuntimeError("version is not set")

    return version


def get_requirements():
    pfile = Project(chdir=False).parsed_pipfile
    requirements = convert_deps_to_pip(pfile["packages"], r=False)
    return requirements


setup(
    name="binman",
    author="purposed",
    url="https://github.com/purposed/binman",
    version=get_version(),
    packages=find_packages(),
    description="Purposed-format binary application manager",
    entry_points={"console_scripts": ["binman=binman.main:cli"]},
    install_requires=get_requirements(),
)
