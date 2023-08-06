import setuptools
from pathlib import Path

setuptools.setup(
    name="sripdf",
    version=1.0,
    long_description=Path("READ.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"]))
