#! /usr/bin/env python

from setuptools import setup, find_packages
from os.path import join
import sys

# Read the natsort.py file for the module version number
import re
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
DESCRIPTION = 'Sort lists naturally'
try:
    with open('README.rst') as fl:
        LONG_DESCRIPTION = fl.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

# python2.6 needs the argparse module
REQUIRES = 'argparse' if sys.version[:3] == '2.6' else ''

# The setup parameters
setup(name='natsort',
      version=VERSION,
      author='Seth M. Morton',
      author_email='drtuba78@gmail.com',
      url='https://github.com/SethMMorton/natsort',
      license='MIT',
      install_requires=REQUIRES,
      packages=find_packages(),
      entry_points={'console_scripts':['natsort = natsort.__main__:main']},
      test_suite='natsort.natsort.test',
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      classifiers=(
        #'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
      )
     )
