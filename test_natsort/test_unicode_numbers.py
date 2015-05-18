# -*- coding: utf-8 -*-
"""\
Test the Unicode numbers module.
"""
from __future__ import unicode_literals
import unicodedata
from natsort.py23compat import py23_range, py23_unichr
from natsort.unicode_numbers import numeric_chars, numeric, digit_chars, digits


def test_numeric_chars_contains_only_valid_unicode_numeric_characters():
    for a in numeric_chars:
        assert unicodedata.numeric(a, None) is not None


def test_digit_chars_contains_only_valid_unicode_digit_characters():
    for a in digit_chars:
        assert unicodedata.digit(a, None) is not None


def test_numeric_chars_contains_all_valid_unicode_numeric_characters():
    for i in py23_range(0X10FFFF):
        try:
            a = py23_unichr(i)
        except ValueError:
            break
        if a in set('0123456789'):
            continue
        if unicodedata.numeric(a, None) is not None:
            assert a in numeric_chars


def test_digit_chars_contains_all_valid_unicode_digit_characters():
    for i in py23_range(0X10FFFF):
        try:
            a = py23_unichr(i)
        except ValueError:
            break
        if a in set('0123456789'):
            continue
        if unicodedata.digit(a, None) is not None:
            assert a in digit_chars


def test_combined_string_contains_all_characters_in_list():
    assert numeric == ''.join(numeric_chars)
    assert digits == ''.join(digit_chars)
