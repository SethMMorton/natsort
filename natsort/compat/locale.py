"""
Compatibility interface for locale fuctionality.

Makes uniform API to either local or PyICU.
"""

from __future__ import annotations

import sys
from typing import Callable, Union

StrOrBytes = Union[str, bytes]
TrxfmFunc = Callable[[str], StrOrBytes]

# This string should be sorted after any other byte string because
# it contains the max unicode character repeated 20 times.
# You would need some odd data to come after that.
null_string = ""
null_string_max = chr(sys.maxunicode) * 20

# This variable could be str or bytes depending on the locale library
# being used, so give the type-checker this information.
null_string_locale: StrOrBytes
null_string_locale_max: StrOrBytes

# strxfrm can be buggy (especially on OSX and *possibly* some other
# BSD-based systems), so prefer icu if available.
try:
    from locale import getlocale

    import icu

    null_string_locale = b""

    # This string should in theory be sorted after any other byte
    # string because it contains the max byte char repeated many times.
    # You would need some odd data to come after that.
    null_string_locale_max = b"x7f" * 50

    def dumb_sort() -> bool:
        """Determine if the locale backend is not collating correctly."""
        return False

    # If using icu, get the locale from the current global locale,
    def get_icu_locale() -> str:
        """Return the current locale as understood by ICU."""
        language_code, encoding = getlocale()
        if language_code is None or encoding is None:  # pragma: no cover
            return icu.Locale()
        return icu.Locale(f"{language_code}.{encoding}")

    def get_strxfrm() -> TrxfmFunc:
        """Return a strxfrm function."""
        return icu.Collator.createInstance(get_icu_locale()).getSortKey

    def get_thousands_sep() -> str:
        """Return the appropriate thousands seperator for this locale."""
        sep = icu.DecimalFormatSymbols.kGroupingSeparatorSymbol
        return icu.DecimalFormatSymbols(get_icu_locale()).getSymbol(sep)

    def get_decimal_point() -> str:
        """Return the appropriate decimal point for this locale."""
        sep = icu.DecimalFormatSymbols.kDecimalSeparatorSymbol
        return icu.DecimalFormatSymbols(get_icu_locale()).getSymbol(sep)

except ImportError:
    import locale
    from locale import strxfrm

    null_string_locale = null_string
    null_string_locale_max = null_string_max

    # On some systems, locale is broken and does not sort in the expected
    # order. We will try to detect this and compensate.
    def dumb_sort() -> bool:
        """Determine if the locale backend is not collating correctly."""
        return strxfrm("A") < strxfrm("a")

    def get_strxfrm() -> TrxfmFunc:
        """Return a strxfrm function."""
        return strxfrm

    def get_thousands_sep() -> str:
        """Return the appropriate thousands seperator for this locale."""
        sep = locale.localeconv()["thousands_sep"]
        # If this locale library is broken, some of the thousands separator
        # characters are incorrectly blank. Here is a lookup table of the
        # corrections I am aware of.
        if dumb_sort():
            language_code, encoding = locale.getlocale()
            if language_code is None or encoding is None:
                # No locale loaded, default to ','
                return ","
            loc = f"{language_code}.{encoding}"
            return {
                "de_DE.ISO8859-15": ".",
                "es_ES.ISO8859-1": ".",
                "de_AT.ISO8859-1": ".",
                "de_at": "\xa0",
                "nl_NL.UTF-8": ".",
                "es_es": ".",
                "fr_CH.ISO8859-15": "\xa0",
                "fr_CA.ISO8859-1": "\xa0",
                "de_CH.ISO8859-1": ".",
                "fr_FR.ISO8859-15": "\xa0",
                "nl_NL.ISO8859-1": ".",
                "ca_ES.UTF-8": ".",
                "nl_NL.ISO8859-15": ".",
                "de_ch": "'",
                "ca_es": ".",
                "de_AT.ISO8859-15": ".",
                "ca_ES.ISO8859-1": ".",
                "de_AT.UTF-8": ".",
                "es_ES.UTF-8": ".",
                "fr_fr": "\xa0",
                "es_ES.ISO8859-15": ".",
                "de_DE.ISO8859-1": ".",
                "nl_nl": ".",
                "fr_ch": "\xa0",
                "fr_ca": "\xa0",
                "de_DE.UTF-8": ".",
                "ca_ES.ISO8859-15": ".",
                "de_CH.ISO8859-15": ".",
                "fr_FR.ISO8859-1": "\xa0",
                "fr_CH.ISO8859-1": "\xa0",
                "de_de": ".",
                "fr_FR.UTF-8": "\xa0",
                "fr_CA.ISO8859-15": "\xa0",
            }.get(loc, sep)
        return sep

    def get_decimal_point() -> str:
        """Return the appropriate decimal point for this locale."""
        return locale.localeconv()["decimal_point"]
