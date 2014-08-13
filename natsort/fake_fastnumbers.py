# -*- coding: utf-8 -*-
"""\
This module is intended to replicate some of the functionality
from the fastnumbers module in the event that module is not
installed.
"""
from __future__ import (print_function, division,
                        unicode_literals, absolute_import)

import re

float_re = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$')
int_re = re.compile(r'[-+]?\d+$')


def fast_float(x, regex_matcher=float_re.match):
    """Convert a string to a float quickly"""
    return float(x) if regex_matcher(x) else x


def fast_int(x, regex_matcher=int_re.match):
    """\
    Convert a string to a int quickly, return input as-is if not possible.
    """
    return int(x) if regex_matcher(x) else x


def isreal(x, ntypes=set([int, float])):
    """Returns true if the input is a real number, false otherwise."""
    return type(x) in ntypes
