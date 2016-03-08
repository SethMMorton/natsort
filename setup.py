#! /usr/bin/env python

# Std. lib imports
import re
import sys
from os.path import join

# Non-std lib imports
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """Custom command to run pytest on all code."""

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        return pytest.main(['--cov', 'natsort',
                            '--cov-report', 'term-missing',
                            '--flakes',
                            '--pep8',
                            # '-s',
                            # '--failed',
                            # '-v',
                            'test_natsort',
                            'README.rst',
                            'docs/source/intro.rst',
                            'docs/source/examples.rst',
                            ])


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
DESCRIPTION = 'Sort lists naturally'
try:
    with open('README.rst') as fl:
        LONG_DESCRIPTION = fl.read()
except IOError:
    LONG_DESCRIPTION = DESCRIPTION

# The argparse module was introduced in python 2.7 or python 3.2
REQUIRES = 'argparse' if sys.version[:3] in ('2.6', '3.0', '3.1') else ''

# Testing needs pytest, and mock if less than python 3.3
TESTS_REQUIRE = ['pytest', 'pytest-pep8', 'pytest-flakes',
                 'pytest-cov', 'pytest-cache', 'hypothesis']

if (sys.version.startswith('2') or
        (sys.version.startswith('3') and int(sys.version.split('.')[1]) < 3)):
    TESTS_REQUIRE.append('mock')
if (sys.version.startswith('2') or
        (sys.version.startswith('3') and int(sys.version.split('.')[1]) < 4)):
    TESTS_REQUIRE.append('pathlib')

# The setup parameters
setup(
    name='natsort',
    version=VERSION,
    author='Seth M. Morton',
    author_email='drtuba78@gmail.com',
    url='https://github.com/SethMMorton/natsort',
    license='MIT',
    install_requires=REQUIRES,
    packages=find_packages(exclude=['test*']),
    entry_points={'console_scripts': ['natsort = natsort.__main__:main']},
    tests_require=TESTS_REQUIRE,
    cmdclass={'test': PyTest},
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=(
        b'Development Status :: 5 - Production/Stable',
        b'Intended Audience :: Developers',
        b'Intended Audience :: Science/Research',
        b'Intended Audience :: System Administrators',
        b'Intended Audience :: Information Technology',
        b'Operating System :: OS Independent',
        b'License :: OSI Approved :: MIT License',
        b'Natural Language :: English',
        b'Programming Language :: Python :: 2.6',
        b'Programming Language :: Python :: 2.7',
        b'Programming Language :: Python :: 3',
        b'Topic :: Scientific/Engineering :: Information Analysis',
        b'Topic :: Utilities',
    )
)
