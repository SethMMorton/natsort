"""\
Test the Unicode numbers module.
"""

from __future__ import annotations

import unicodedata
import warnings

from natsort.unicode import UnicodeNumbers
from natsort.unicode.decimal_hex import hex_values as decimal_hex
from natsort.unicode.digit_hex import hex_values as digit_hex
from natsort.unicode.numeric_hex import hex_values as numeric_hex


def test_numeric_chars_contains_only_valid_unicode_numeric_characters() -> None:
    for a in UnicodeNumbers.numeric_chars():
        assert unicodedata.numeric(a, None) is not None


def test_digit_chars_contains_only_valid_unicode_digit_characters() -> None:
    for a in UnicodeNumbers.digit_chars():
        assert unicodedata.digit(a, None) is not None


def test_decimal_chars_contains_only_valid_unicode_decimal_characters() -> None:
    for a in UnicodeNumbers.decimal_chars():
        assert unicodedata.decimal(a, None) is not None


def test_numeric_chars_contains_all_valid_unicode_numeric_and_digit_characters() -> (
    None
):
    set_numeric_chars = set(UnicodeNumbers.numeric_chars())
    set_digit_chars = set(UnicodeNumbers.digit_chars())
    set_decimal_chars = set(UnicodeNumbers.decimal_chars())

    assert set_decimal_chars.isdisjoint(UnicodeNumbers.digits_no_decimals())
    assert set_digit_chars.issuperset(UnicodeNumbers.digits_no_decimals())

    assert set_decimal_chars.isdisjoint(UnicodeNumbers.numeric_no_decimals())
    assert set_numeric_chars.issuperset(UnicodeNumbers.numeric_no_decimals())


def test_missing_unicode_numeral_in_collection() -> None:
    ok = True
    set_numeric_hex = set(numeric_hex)
    for i in range(0x110000):
        try:
            a = chr(i)
        except ValueError:
            break
        if a in "0123456789":
            continue
        if unicodedata.numeric(a, None) is not None:  # noqa: SIM102
            if i not in set_numeric_hex:
                ok = False
    if not ok:
        warnings.warn(
            """\
Not all numeric unicode characters are represented in natsort/unicode/numeral_hex.py.
This can be addressed by running dev/generate_new_unicode_numbers.py with the current \
version of Python.
It would be much appreciated if you would submit a Pull Request to the natsort
repository (https://github.com/SethMMorton/natsort) with the resulting change.
""",
            stacklevel=2,
        )


def test_missing_unicode_digit_in_collection() -> None:
    ok = True
    set_digit_hex = set(digit_hex)
    for i in range(0x110000):
        try:
            a = chr(i)
        except ValueError:
            break
        if a in "0123456789":
            continue
        if unicodedata.digit(a, None) is not None:  # noqa: SIM102
            if i not in set_digit_hex:
                ok = False
    if not ok:
        warnings.warn(
            """\
Not all numeric unicode characters are represented in natsort/unicode/digit_hex.py.
This can be addressed by running dev/generate_new_unicode_numbers.py with the current \
version of Python.
It would be much appreciated if you would submit a Pull Request to the natsort
repository (https://github.com/SethMMorton/natsort) with the resulting change.
""",
            stacklevel=2,
        )


def test_missing_unicode_decimal_in_collection() -> None:
    ok = True
    set_decimal_hex = set(decimal_hex)
    for i in range(0x110000):
        try:
            a = chr(i)
        except ValueError:
            break
        if a in "0123456789":
            continue
        if unicodedata.decimal(a, None) is not None:  # noqa: SIM102
            if i not in set_decimal_hex:
                ok = False
    if not ok:
        warnings.warn(
            """\
Not all numeric unicode characters are represented in natsort/unicode/decimal_hex.py.
This can be addressed by running dev/generate_new_unicode_numbers.py with the current \
version of Python.
It would be much appreciated if you would submit a Pull Request to the natsort
repository (https://github.com/SethMMorton/natsort) with the resulting change.
""",
            stacklevel=2,
        )


def test_combined_string_contains_all_characters_in_list() -> None:
    assert UnicodeNumbers.numeric() == "".join(UnicodeNumbers.numeric_chars())
    assert UnicodeNumbers.digits() == "".join(UnicodeNumbers.digit_chars())
    assert UnicodeNumbers.decimal() == "".join(UnicodeNumbers.decimal_chars())
