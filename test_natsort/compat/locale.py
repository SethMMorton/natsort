# -*- coding: utf-8 -*-
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# Std. lib imports.
import locale

# Local imports
from natsort.compat.py23 import py23_str, py23_unichr, py23_range


def load_locale(x):
    """ Convenience to load a locale, trying ISO8859-1 first."""
    try:
        locale.setlocale(locale.LC_ALL, str('{0}.ISO8859-1'.format(x)))
    except locale.Error:
        locale.setlocale(locale.LC_ALL, str('{0}.UTF-8'.format(x)))

# Check if de_DE is installed.
try:
    load_locale('de_DE')
    has_locale_de_DE = True
except locale.Error:
    has_locale_de_DE = False

# Depending on the python version, use lower or casefold
# to make a string lowercase.
try:
    low = py23_str.casefold
except AttributeError:
    low = py23_str.lower

# There are some unicode values that are known failures on BSD systems
# that has nothing to do with natsort (a ValueError is raised by strxfrm).
# Let's filter them out.
try:
    bad_uni_chars = set(py23_unichr(x) for x in py23_range(0X10fefd,
                                                           0X10ffff+1))
except ValueError:
    # Narrow unicode build... no worries.
    bad_uni_chars = set()
