# -*- coding: utf-8 -*-
"""\
This module is intended to help combine some locale functions
together for natsort consumption.  It also accounts for Python2
and Python3 differences.
"""
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# Std. lib imports.
from itertools import chain

# Local imports.
from natsort.compat.locale import use_pyicu, _low
if use_pyicu:
    from natsort.compat.locale import get_pyicu_transform, getlocale
else:
    from natsort.compat.locale import strxfrm


def groupletters(x):
    """Double all characters, making doubled letters lowercase."""
    return ''.join(chain.from_iterable([_low(y), y] for y in x))


def locale_convert(x):
    """
    Use the appropriate locale tranformation function on the given input.
    """
    if use_pyicu:
        return get_pyicu_transform(getlocale())(x)
    else:
        return strxfrm(x)
