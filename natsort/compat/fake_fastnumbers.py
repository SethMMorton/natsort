# -*- coding: utf-8 -*-
"""\
This module is intended to replicate some of the functionality
from the fastnumbers module in the event that module is not
installed.
"""
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# Std. lib imports.
import sys
import unicodedata
if sys.version[0] != '2':
    long = int


nan_inf = set(['INF', 'INf', 'Inf', 'inF', 'iNF', 'InF', 'inf', 'iNf',
               'NAN', 'nan', 'NaN', 'nAn', 'naN', 'NAn', 'nAN', 'Nan'])


def fast_float(x, uni=unicodedata.numeric, nan_inf=nan_inf):
    """\
    Convert a string to a float quickly, return input as-is if not possible.
    We don't need to accept all input that the real fast_int accepts because
    the input will be controlled by the splitting algorithm.
    """
    if type(x) in (int, long, float):
        return float(x)
    elif x[0] in '0123456789+-.' or x[:3] in nan_inf:
        try:
            return float(x)
        except ValueError:
            return uni(x, x) if len(x) == 1 else x
    else:
        return uni(x, x) if len(x) == 1 else x


def fast_int(x, uni=unicodedata.digit):
    """\
    Convert a string to a int quickly, return input as-is if not possible.
    We don't need to accept all input that the real fast_int accepts because
    the input will be controlled by the splitting algorithm.
    """
    if type(x) in (int, long, float):
        return int(x)
    elif x[0] in '0123456789+-':
        try:
            return int(x)
        except ValueError:
            return uni(x, x) if len(x) == 1 else x
    else:
        return uni(x, x) if len(x) == 1 else x


def isfloat(x, num_only=False):
    """Returns true if the input is a float, false otherwise."""
    return type(x) == float


def isint(x, num_only=False):
    """Returns true if the input is an int, false otherwise."""
    return type(x) in set([int, long])
