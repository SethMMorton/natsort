#! /usr/bin/env python

# Std. lib imports
import re
from os.path import join

# Non-std lib imports
from setuptools import setup, find_packages

# Read the natsort.py file for the module version number
VERSIONFILE = join('natsort', '_version.py')
versionsearch = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]")
with open(VERSIONFILE, "rt") as fl:
    for line in fl:
        m = versionsearch.search(line)
        if m:
            VERSION = m.group(1)
            break
    else:
        s = "Unable to locate version string in {0}"
        raise RuntimeError(s.format(VERSIONFILE))

# Read in the documentation for the long_description
DESCRIPTION = 'Simple yet flexible natural sorting in Python.'
try:
    with open('README.rst') as fl:
        LONG_DESCRIPTION = fl.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

# The setup parameters
setup(
    name='natsort',
    version=VERSION,
    author='Seth M. Morton',
    author_email='drtuba78@gmail.com',
    url='https://github.com/SethMMorton/natsort',
    license='MIT',
    packages=find_packages(exclude=['test*']),
    entry_points={'console_scripts': ['natsort = natsort.__main__:main']},
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Financial and Insurance Industry',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
        'Topic :: Text Processing',
    )
)
