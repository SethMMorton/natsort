# -*- coding: utf-8 -*-
"""\
This module is intended to help combine some locale functions
together for natsort consumption.  It also accounts for Python2
and Python3 differences.
"""
from __future__ import (print_function, division,
                        unicode_literals, absolute_import)

# Std. lib imports.
import sys
from itertools import chain
from locale import localeconv

# Local imports.
from natsort.py23compat import py23_zip

# We need cmp_to_key for Python2 because strxfrm is broken for unicode.
if sys.version[:3] == '2.7':
    from functools import cmp_to_key
# cmp_to_key was not created till 2.7.
elif sys.version[:3] == '2.6':
    def cmp_to_key(mycmp):
        """Convert a cmp= function into a key= function"""
        class K(object):  # pragma: no cover
            __slots__ = ['obj']

            def __init__(self, obj):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0

            def __hash__(self):
                raise TypeError('hash not implemented')

        return K

# Make the strxfrm function from strcoll on Python2
# It can be buggy, so prefer PyICU if available.
try:
    import PyICU
    from locale import getlocale

    # If using PyICU, get the locale from the current global locale,
    # then create a sort key from that
    def get_pyicu_transform(l, _d={}):
        if l not in _d:
            if l == (None, None):
                c = PyICU.Collator.createInstance(PyICU.Locale())
            else:
                loc = '.'.join(l)
                c = PyICU.Collator.createInstance(PyICU.Locale(loc))
            _d[l] = c.getSortKey
        return _d[l]
    use_pyicu = True
except ImportError:
    if sys.version[0] == '2':
        from locale import strcoll
        strxfrm = cmp_to_key(strcoll)
    else:
        from locale import strxfrm
    use_pyicu = False

# This little lambda doubles all characters, making letters lowercase.
groupletters = lambda x: ''.join(chain(*py23_zip(x.lower(), x)))


def grouper(val, func):
    """\
    Attempt to convert a string to a number.  If the conversion
    was not possible, run it through the letter grouper
    to make the sorting work as requested.
    """
    # Return the number or transformed string.
    # If the input is identical to the output, then no conversion happened.
    s = func(val)
    return groupletters(s) if val is s else s


def locale_convert(val, func, group):
    """\
    Attempt to convert a string to a number, first converting
    the decimal place character if needed. Then, if the conversion
    was not possible, run it through strxfrm to make the sorting
    as requested, possibly grouping first.
    """

    # Format the number so that the conversion function can interpret it.
    radix = localeconv()['decimal_point']
    s = val.replace(radix, '.') if radix != '.' else val

    # Perform the conversion
    t = func(s)

    # Return the number or transformed string.
    # If the input is identical to the output, then no conversion happened.
    # In this case, we don't want to return the function output because it
    # may have had characters modified from the above 'replace' call,
    # so we return the input.
    if group:
        if use_pyicu:
            xfrm = get_pyicu_transform(getlocale())
            return xfrm(groupletters(val)) if s is t else t
        else:
            return strxfrm(groupletters(val)) if s is t else t
    else:
        if use_pyicu:
            xfrm = get_pyicu_transform(getlocale())
            return xfrm(val) if s is t else t
        else:
            return strxfrm(val) if s is t else t
