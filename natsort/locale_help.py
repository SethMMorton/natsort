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
from locale import localeconv

# Local imports.
from natsort.compat.locale import use_pyicu, _low
if use_pyicu:
    from natsort.compat.locale import get_pyicu_transform, getlocale
else:
    from natsort.compat.locale import strxfrm


def groupletters(x):
    """Double all characters, making doubled letters lowercase."""
    return ''.join(chain.from_iterable([_low(y), y] for y in x))


def grouper(val, func):
    """\
    Attempt to convert a string to a number.  If the conversion
    was not possible, run it through the letter grouper
    to make the sorting work as requested.
    """
    # Return the number or transformed string.
    # If the input is identical to the output, then no conversion happened.
    s = func[0](val)
    return groupletters(s) if not func[1](s) else s


def locale_convert(val, func, group):
    """\
    Attempt to convert a string to a number, first converting
    the decimal place character if needed. Then, if the conversion
    was not possible (i.e. it is not a number), run it through
    strxfrm to make the work sorting as requested, possibly grouping first.
    """

    # Format the number so that the conversion function can interpret it.
    radix = localeconv()['decimal_point']
    s = val.replace(radix, '.') if radix != '.' else val

    # Perform the conversion
    t = func[0](s)

    # Return the number or transformed string.
    # If the input is identical to the output, then no conversion happened.
    # In this case, we don't want to return the function output because it
    # may have had characters modified from the above 'replace' call,
    # so we return the input.
    if group:
        if use_pyicu:
            xfrm = get_pyicu_transform(getlocale())
            return xfrm(groupletters(val)) if not func[1](t) else t
        else:
            return strxfrm(groupletters(val)) if not func[1](t) else t
    else:
        if use_pyicu:
            xfrm = get_pyicu_transform(getlocale())
            return xfrm(val) if not func[1](t) else t
        else:
            return strxfrm(val) if not func[1](t) else t
