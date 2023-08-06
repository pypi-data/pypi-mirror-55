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

README_FILE = Path(__file__).resolve().with_name("README.md")
README = README_FILE.read_text("utf-8")


setup(
    name="pystatsd-tags",
    packages=find_packages(exclude=["tests"]),
    extras_require={"test": ["pytest", "coverage"], "docs": ["sphinx"]},
    version="0.0.3",
    description="Datadog tags implementation for statsd.",
    author="Sam Pegler",
    author_email="sam@sampegler.co.uk",
    license="MIT",
    tests_require=["nose", "pytest", "mock"],
    python_requires=">3.6.0",
)
