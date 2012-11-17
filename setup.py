#! /usr/bin/env python

# In case setuptools is not installed
import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup
from os.path import join

# Read the _version.py file for the module version number
import re
VERSIONFILE = 'natsort.py'
with open(VERSIONFILE, "rt") as fl:
    versionstring = fl.readline().strip()
m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", versionstring)
if m:
    version = m.group(1)
else:
    s = "Unable to locate version string in {0}"
    raise RuntimeError (s.format(VERSIONFILE))

setup(name='natsort',
      version=version,
      author='Seth M. Morton',
      author_email='drtuba78@gmail.com',
      url='https://github.com/SethMMorton/natsort',
      #download_url='',
      py_modules=['natsort'],
      scripts=[join('scripts', 'natsort')],
      description='Provides routines and a command-line script to sort lists naturally',
      #long_description='',
     )
