#! /usr/bin/env python

import sys

from setuptools import find_packages, setup

# Very old versions of setuptools do not support the python version
# specifier syntax, so logic must be defined in code (see issue #64).
install_requires = []
extras_require = {"icu": "PyICU >= 1.0.0"}
if sys.version_info[:2] == (2, 6):
    install_requires.append("argparse")
else:
    extras_require["fast"] = "fastnumbers >= 2.0.0"

setup(
    name='natsort',
    version='5.5.0',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={'console_scripts': ['natsort = natsort.__main__:main']},
    extras_require=extras_require,
)
