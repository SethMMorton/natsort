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
float_re = re.compile(r'[-+]?(\d*\.?\d+(?:[eE][-+]?\d+)?|inf(?:inity)?|nan)$')
if sys.version[0] == '2':
    int_re = re.compile(r'[-+]?\d+[lL]?$')
else:
    int_re = re.compile(r'[-+]?\d+$')
    long = int


def fast_float(x, regex_matcher=float_re.match):
    """Convert a string to a float quickly"""
    return float(x) if regex_matcher(x) else x


def fast_int(x, regex_matcher=int_re.match):
    """\
    Convert a string to a int quickly, return input as-is if not possible.
    """
    return long(x) if regex_matcher(x) else x


def isfloat(x, num_only=False):
    """Returns true if the input is a float, false otherwise."""
    return type(x) == float


def isint(x, num_only=False):
    """Returns true if the input is an int, false otherwise."""
    return type(x) in set([int, long])
