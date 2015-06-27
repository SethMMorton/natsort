# -*- coding: utf-8 -*-
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# Std. lib imports
import sys

# Local imports.
from natsort.compat.py23 import PY_VERSION, cmp_to_key

# Make the strxfrm function from strcoll on Python2
# It can be buggy (especially on BSD-based systems),
# so prefer PyICU if available.
try:
    import PyICU
    from locale import getlocale

    # If using PyICU, get the locale from the current global locale,
    # then create a sort key from that
    def get_pyicu_transform(l, _d={}):
        if l not in _d:
            if l == (None, None):  # pragma: no cover
                c = PyICU.Collator.createInstance(PyICU.Locale())
            else:
                loc = '.'.join(l)
                c = PyICU.Collator.createInstance(PyICU.Locale(loc))
            _d[l] = c.getSortKey
        return _d[l]
    use_pyicu = True
    null_string = b''

    def dumb_sort():
        return False
except ImportError:
    if sys.version[0] == '2':
        from locale import strcoll
        strxfrm = cmp_to_key(strcoll)
        null_string = strxfrm('')
    else:
        from locale import strxfrm
        null_string = ''
    use_pyicu = False

    # On some systems, locale is broken and does not sort in the expected
    # order. We will try to detect this and compensate.
    def dumb_sort():
        return strxfrm('A') < strxfrm('a')


if PY_VERSION >= 3.3:
    def _low(x):
        return x.casefold()
else:
    def _low(x):
        return x.lower()
