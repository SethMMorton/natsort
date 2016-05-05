# -*- coding: utf-8 -*-
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# Local imports.
from natsort.compat.py23 import PY_VERSION, cmp_to_key

# Make the strxfrm function from strcoll on Python2
# It can be buggy (especially on BSD-based systems),
# so prefer PyICU if available.
try:
    import PyICU
    from locale import getlocale

    null_string = b''

    # If using PyICU, get the locale from the current global locale,
    def get_icu_locale():
        try:
            return PyICU.Locale('.'.join(getlocale()))
        except TypeError:  # pragma: no cover
            return PyICU.Locale()

    def get_strxfrm():
        return PyICU.Collator.createInstance(get_icu_locale()).getSortKey

    def get_thousands_sep():
        sep = PyICU.DecimalFormatSymbols.kGroupingSeparatorSymbol
        return PyICU.DecimalFormatSymbols(get_icu_locale()).getSymbol(sep)

    def get_decimal_point():
        sep = PyICU.DecimalFormatSymbols.kDecimalSeparatorSymbol
        return PyICU.DecimalFormatSymbols(get_icu_locale()).getSymbol(sep)

    def dumb_sort():
        return False

except ImportError:
    import locale
    if PY_VERSION < 3:
        from locale import strcoll
        strxfrm = cmp_to_key(strcoll)
        null_string = strxfrm('')
    else:
        from locale import strxfrm
        null_string = ''

    def get_strxfrm():
        return strxfrm

    def get_thousands_sep():
        return locale.localeconv()['thousands_sep']

    def get_decimal_point():
        return locale.localeconv()['decimal_point']

    # On some systems, locale is broken and does not sort in the expected
    # order. We will try to detect this and compensate.
    def dumb_sort():
        return strxfrm('A') < strxfrm('a')
