#! /usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from os.path import join

# Read the natsort.py file for the module version number
import re
VERSIONFILE = 'natsort.py'
with open(VERSIONFILE, "rt") as fl:
    versionstring = fl.readline().strip()
m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", versionstring)
if m:
    VERSION = m.group(1)
else:
    s = "Unable to locate version string in {0}"
    raise RuntimeError (s.format(VERSIONFILE))

# A description
DESCRIPTION = ('Provides routines and a command-line script to sort lists '
               'naturally')

# Read in the documentation for the long_description
try:
    with open('README.rst') as fl:
        LONG_DESCRIPTION = fl.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

# The setup parameters
setup(name='natsort',
      version=VERSION,
      author='Seth M. Morton',
      author_email='drtuba78@gmail.com',
      url='https://github.com/SethMMorton/natsort',
      license='MIT',
      py_modules=['natsort'],
      scripts=[join('scripts', 'natsort')],
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: Freeware',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
      )
     )
