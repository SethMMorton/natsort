# -*- coding: utf-8 -*-
"""\
Test the locale help module module.
"""
from __future__ import unicode_literals

import locale
import pytest
from math import isnan
from itertools import chain
from natsort.compat.fake_fastnumbers import fast_float
from natsort.locale_help import groupletters, locale_convert
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


def test_groupletters_returns_letters_with_lowercase_transform_of_letter_example():
    assert groupletters('HELLO') == 'hHeElLlLoO'
    assert groupletters('hello') == 'hheelllloo'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_groupeletters_returns_letters_with_lowercase_transform_of_letter(x):
    assume(bool(x))
    assume(type(fast_float(x)) is not float)
    assert groupletters(x) == ''.join(chain.from_iterable([low(y), y] for y in x))


def test_groupletters_returns_letters_with_lowercase_transform_of_letter_after_applying_key_example():
    assert groupletters('HELLO', key=lambda x: x.lower()) == 'hheelllloo'
    assert groupletters('hello', key=lambda x: x.lower()) == 'hheelllloo'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_groupeletters_returns_letters_with_lowercase_transform_of_letter_after_applying_key(x):
    assume(bool(x))
    assume(type(fast_float(x)) is not float)
    assert groupletters(x, key=lambda x: x.lower()) == ''.join(chain.from_iterable([low(y), y] for y in x.lower()))


def test_locale_convert_transforms_string_to_strxfrm_string_example():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert('45,8') == strxfrm('45,8')
    assert locale_convert('hello') == strxfrm('hello')
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_locale_convert_transforms_string_to_strxfrm_string(x):
    assume(bool(x))
    assume(type(fast_float(x)) is not float)
    assume(not any(i in bad_uni_chars for i in x))
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert(x) == strxfrm(x)
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters_example():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert('hello', key=groupletters) == strxfrm('hheelllloo')
    assert locale_convert('45,8', key=groupletters) == strxfrm('4455,,88')
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters(x):
    assume(bool(x))
    assume(type(fast_float(x)) is not float)
    assume(not any(i in bad_uni_chars for i in x))
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert locale_convert(x, key=groupletters) == strxfrm(''.join(chain.from_iterable([low(y), y] for y in x)))
    locale.setlocale(locale.LC_NUMERIC, str(''))
