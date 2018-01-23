#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


#--- Imports ---

# Python Classes
import re
from setuptools import setup


#--- Main ---

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('botospy/BotoSpy.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "BotoSpy",
    packages = ["botospy"],
    entry_points = {
        "console_scripts": ['botospy = botospy.BotoSpy:main']
        },
    version = version,
    description = "Python command line application and library for watching or mocking the boto3 / AWS Python api / aws command line",
    long_description = long_descr,
    author = "Philip Bowditch",
    author_email = "a@b.com",
    url = "",
    )
