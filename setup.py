#! /usr/bin/env python

# In case setuptools is not installed
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup
from os.path import join

setup(name='natsort',
      version='1.2',
      author='Seth M. Morton',
      author_email='drtuba78@gmail.com',
      url='https://github.com/SethMMorton/natsort',
      #download_url='',
      py_modules=['natsort'],
      scripts=[join('scripts', 'natsort')],
      description='Provides routines and a command-line script to sort lists naturally',
      #long_description='',
     )
