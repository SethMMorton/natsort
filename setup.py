#! /usr/bin/env python

from setuptools import find_packages, setup
setup(
    name='natsort',
    version='6.2.1',
    packages=find_packages(),
    entry_points={'console_scripts': ['natsort = natsort.__main__:main']},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    extras_require={
        'fast': ["fastnumbers >= 2.0.0"],
        'icu': ["PyICU >= 1.0.0"]
    }
)
