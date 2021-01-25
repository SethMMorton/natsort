#! /usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="natsort",
    version="7.1.1",
    packages=find_packages(),
    entry_points={"console_scripts": ["natsort = natsort.__main__:main"]},
    python_requires=">=3.4",
    extras_require={"fast": ["fastnumbers >= 2.0.0"], "icu": ["PyICU >= 1.0.0"]},
)
