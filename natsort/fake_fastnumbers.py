# -*- coding: utf-8 -*-
"""\
This module is intended to replicate some of the functionality
from the fastnumbers module in the event that module is not
installed.
"""
from __future__ import (print_function, division,
                        unicode_literals, absolute_import)

# Std. lib imports.
import sys
import re
import unicodedata
float_re = re.compile(r'[-+]?(\d*\.?\d+(?:[eE][-+]?\d+)?|inf(?:inity)?|nan)$')
if sys.version[0] == '2':
    int_re = re.compile(r'[-+]?\d+[lL]?$')
else:
    int_re = re.compile(r'[-+]?\d+$')
    long = int
    unicode = str


def fast_float(x, regex_matcher=float_re.match, uni=unicodedata.numeric):
    """Convert a string to a float quickly"""
    if type(x) in (int, long, float):
        return float(x)
    elif regex_matcher(x):
        return float(x)
    elif type(x) == unicode and len(x) == 1 and uni(x, None) is not None:
        return uni(x)
    else:
        return x


def fast_int(x, regex_matcher=int_re.match, uni=unicodedata.digit):
    """\
    Convert a string to a int quickly, return input as-is if not possible.
    """
    if type(x) in (int, long, float):
        return int(x)
    elif regex_matcher(x):
        return int(x.rstrip('Ll'))
    elif type(x) == unicode and len(x) == 1 and uni(x, None) is not None:
        return uni(x)
    else:
        return x


def isfloat(x, num_only=False):
    """Returns true if the input is a float, false otherwise."""
    return type(x) == float


def isint(x, num_only=False):
    """Returns true if the input is an int, false otherwise."""
    return type(x) in set([int, long])
