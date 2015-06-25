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
from natsort.locale_help import use_pyicu
from natsort.compat.py23 import py23_str


def load_locale(x):
    """ Convenience to load a locale, trying ISO8859-1 first."""
    try:
        locale.setlocale(locale.LC_ALL, str('{}.ISO8859-1'.format(x)))
    except:
        locale.setlocale(locale.LC_ALL, str('{}.UTF-8'.format(x)))

# Check if de_DE is installed.
try:
    load_locale('de_DE')
    has_locale_de_DE = True
except locale.Error:
    has_locale_de_DE = False

# Make a function that will return the appropriate
# strxfrm for the current locale.
if use_pyicu:
    from natsort.locale_help import get_pyicu_transform
    from locale import getlocale

    def get_strxfrm():
        return get_pyicu_transform(getlocale())
else:
    from natsort.locale_help import strxfrm

    def get_strxfrm():
        return strxfrm

# Depending on the python version, use lower or casefold
# to make a string lowercase.
try:
    low = py23_str.casefold
except AttributeError:
    low = py23_str.lower
