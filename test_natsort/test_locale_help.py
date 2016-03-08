# -*- coding: utf-8 -*-
"""\
Test the locale help module module.
"""
from __future__ import unicode_literals

import locale
import pytest
from math import isnan
from itertools import chain
from natsort.compat.fake_fastnumbers import fast_float, isfloat
from natsort.locale_help import grouper, locale_convert
from natsort.compat.py23 import py23_str
from natsort.compat.locale import use_pyicu
from compat.locale import (
    load_locale,
    has_locale_de_DE,
    get_strxfrm,
    low,
    bad_uni_chars,
)
from compat.hypothesis import (
    assume,
    given,
    text,
    floats,
    use_hypothesis,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_grouper_returns_letters_with_lowercase_transform_of_letter_example():
    assert grouper('HELLO', (fast_float, isfloat)) == 'hHeElLlLoO'
    assert grouper('hello', (fast_float, isfloat)) == 'hheelllloo'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_grouper_returns_letters_with_lowercase_transform_of_letter(x):
    assume(type(fast_float(x)) is not float)
    assert grouper(x, (fast_float, isfloat)) == ''.join(chain.from_iterable([low(y), y] for y in x))


def test_grouper_returns_float_string_as_float_example():
    assert grouper('45.8e-2', (fast_float, isfloat)) == 45.8e-2


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats())
def test_grouper_returns_float_string_as_float(x):
    assume(not isnan(x))
    assert grouper(repr(x), (fast_float, isfloat)) == x


def test_locale_convert_transforms_float_string_to_float_example():
    load_locale('en_US')
    assert locale_convert('45.8', (fast_float, isfloat), False) == 45.8
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats())
def test_locale_convert_transforms_float_string_to_float(x):
    assume(not isnan(x))
    load_locale('en_US')
    assert locale_convert(repr(x), (fast_float, isfloat), False) == x
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_transforms_nonfloat_string_to_strxfrm_string_example():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert('45,8', (fast_float, isfloat), False) == strxfrm('45,8')
    assert locale_convert('hello', (fast_float, isfloat), False) == strxfrm('hello')
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_locale_convert_transforms_nonfloat_string_to_strxfrm_string(x):
    assume(type(fast_float(x)) is not float)
    assume(not any(i in bad_uni_chars for i in x))
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert(x, (fast_float, isfloat), False) == strxfrm(x)
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters_example():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert('hello', (fast_float, isfloat), True) == strxfrm('hheelllloo')
    assert locale_convert('45,8', (fast_float, isfloat), True) == strxfrm('4455,,88')
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters(x):
    assume(type(fast_float(x)) is not float)
    assume(not any(i in bad_uni_chars for i in x))
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert(x, (fast_float, isfloat), True) == strxfrm(''.join(chain.from_iterable([low(y), y] for y in x)))
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale')
def test_locale_convert_transforms_float_string_to_float_with_de_locale_example():
    load_locale('de_DE')
    assert locale_convert('45.8', (fast_float, isfloat), False) == 45.8
    assert locale_convert('45,8', (fast_float, isfloat), False) == 45.8
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale')
@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats())
def test_locale_convert_transforms_float_string_to_float_with_de_locale(x):
    assume(not isnan(x))
    load_locale('de_DE')
    assert locale_convert(repr(x), (fast_float, isfloat), False) == x
    assert locale_convert(repr(x).replace('.', ','), (fast_float, isfloat), False) == x
    locale.setlocale(locale.LC_NUMERIC, str(''))
