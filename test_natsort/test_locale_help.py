# -*- coding: utf-8 -*-
"""\
Test the locale help module module.
"""
import locale
from math import isnan
from itertools import chain
from natsort.fake_fastnumbers import fast_float, isfloat, isint
from natsort.locale_help import grouper, locale_convert, use_pyicu
from natsort.py23compat import py23_str
from hypothesis import given, assume

if use_pyicu:
    from natsort.locale_help import get_pyicu_transform
    from locale import getlocale
    strxfrm = get_pyicu_transform(getlocale())
else:
    from natsort.locale_help import strxfrm

# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_grouper_returns_letters_with_lowercase_transform_of_letter_example():
    assert grouper('HELLO', (fast_float, isfloat)) == 'hHeElLlLoO'
    assert grouper('hello', (fast_float, isfloat)) == 'hheelllloo'


@given(py23_str)
def test_grouper_returns_letters_with_lowercase_transform_of_letter(x):
    assume(type(fast_float(x)) is not float)
    try:
        low = py23_str.casefold
    except AttributeError:
        low = py23_str.lower
    assert grouper(x, (fast_float, isfloat)) == ''.join(chain.from_iterable([low(y), y] for y in x))


def test_grouper_returns_float_string_as_float_example():
    assert grouper('45.8e-2', (fast_float, isfloat)) == 45.8e-2


@given(float)
def test_grouper_returns_float_string_as_float(x):
    assume(not isnan(x))
    assert grouper(repr(x), (fast_float, isfloat)) == x


def test_locale_convert_transforms_float_string_to_float_example():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    assert locale_convert('45.8', (fast_float, isfloat), False) == 45.8
    locale.setlocale(locale.LC_NUMERIC, str(''))


@given(float)
def test_locale_convert_transforms_float_string_to_float(x):
    assume(not isnan(x))
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    assert locale_convert(repr(x), (fast_float, isfloat), False) == x
    locale.setlocale(locale.LC_NUMERIC, str(''))


# The following tests are example only, no hypothesis tests

def test_locale_convert_transforms_nonfloat_string_to_strxfrm_string_example():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert locale_convert('45,8', (fast_float, isfloat), False) == strxfrm('45,8')
    assert locale_convert('hello', (fast_float, isfloat), False) == strxfrm('hello')
    locale.setlocale(locale.LC_NUMERIC, str(''))


@given(py23_str)
def test_locale_convert_transforms_nonfloat_string_to_strxfrm_string(x):
    assume(not x.isdigit())
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert locale_convert(x, (fast_float, isfloat), False) == strxfrm(x)
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters_example():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert locale_convert('hello', (fast_float, isfloat), True) == strxfrm('hheelllloo')
    assert locale_convert('45,8', (fast_float, isfloat), True) == strxfrm('4455,,88')
    locale.setlocale(locale.LC_NUMERIC, str(''))


@given(py23_str)
def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters(x):
    assume(not x.isdigit())
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    try:
        low = py23_str.casefold
    except AttributeError:
        low = py23_str.lower
    assert locale_convert(x, (fast_float, isfloat), True) == strxfrm(u''.join(chain.from_iterable([low(y), y] for y in x)))
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_transforms_float_string_to_float_with_de_locale_example():
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    assert locale_convert('45.8', (fast_float, isfloat), False) == 45.8
    assert locale_convert('45,8', (fast_float, isfloat), False) == 45.8
    locale.setlocale(locale.LC_NUMERIC, str(''))


@given(float)
def test_locale_convert_transforms_float_string_to_float_with_de_locale(x):
    assume(not isnan(x))
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    assert locale_convert(repr(x), (fast_float, isfloat), False) == x
    assert locale_convert(repr(x).replace(u'.', u','), (fast_float, isfloat), False) == x
    locale.setlocale(locale.LC_NUMERIC, str(''))
