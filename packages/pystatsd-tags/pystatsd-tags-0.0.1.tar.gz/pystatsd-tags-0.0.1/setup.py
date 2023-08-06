#!/usr/bin/env python3
"""Auth API setup."""
import sys
import subprocess
import shlex
from pathlib import Path
from typing import List
from setuptools import setup, find_packages  # type: ignore
from setuptools.command.develop import develop  # type: ignore
from distutils.extension import Extension


def parse_reqs(requirements_file: str) -> List[str]:
    """Get requirements as a list of strings from the file."""
    with open(requirements_file) as reqs:
        return [x for x in reqs]


class CustomDevelop(develop):
    """Develop command that actually prepares the development environment."""

    def run(self):
        """Setup the local dev environment fully."""
        super().run()

        for command in [
            "pip --version",
            "pip install -r dev_requirements.txt",
            "pip install -r requirements.txt",
        ]:
            print("\nCustom develop - executing:", command, file=sys.stderr)
            subprocess.check_call(shlex.split(command))


README_FILE = Path(__file__).resolve().with_name("README.md")
README = README_FILE.read_text("utf-8")
REQUIREMENTS = parse_reqs("requirements.txt")
TEST_REQUIREMENTS = parse_reqs("dev_requirements.txt")


setup(
    name="pystatsd-tags",
    packages=find_packages(exclude=["tests"]),
    extras_require={"test": ["pytest", "coverage"], "docs": ["sphinx"]},
    version="0.0.1",
    description="Datadog tags implementation for statsd.",
    author="Sam Pegler",
    author_email="sam@sampegler.co.uk", 
    license="MIT",
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    cmdclass={"develop": CustomDevelop},
    python_requires='>3.6.0',
)
