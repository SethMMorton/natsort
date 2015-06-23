# -*- coding: utf-8 -*-
"""\
Test the fake fastnumbers module.
"""
from __future__ import unicode_literals

import pytest
import unicodedata
from math import isnan
from natsort.fake_fastnumbers import fast_float, fast_int, isfloat, isint
from natsort.compat.py23 import py23_str
from compat.py26 import assume, given, use_hypothesis


def is_float(x):
    try:
        float(x)
    except ValueError:
        try:
            unicodedata.numeric(x)
        except (ValueError, TypeError):
            return False
        else:
            return True
    else:
        return True


def is_int(x):
    try:
        int(x)
    except ValueError:
        try:
            unicodedata.digit(x)
        except (ValueError, TypeError):
            return False
        else:
            return True
    else:
        return True

# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_fast_float_converts_float_string_to_float_example():
    assert fast_float('45.8') == 45.8
    assert fast_float('-45') == -45.0
    assert fast_float('45.8e-2') == 45.8e-2
    assert isnan(fast_float('nan'))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(float)
def test_fast_float_converts_float_string_to_float(x):
    assume(not isnan(x))  # But inf is included
    assert fast_float(repr(x)) == x


def test_fast_float_leaves_string_as_is_example():
    assert fast_float('invalid') == 'invalid'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(py23_str)
def test_fast_float_leaves_string_as_is(x):
    assume(not is_float(x))
    assert fast_float(x) == x


def test_fast_int_leaves_float_string_as_is_example():
    assert fast_int('45.8') == '45.8'
    assert fast_int('nan') == 'nan'
    assert fast_int('inf') == 'inf'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(float)
def test_fast_int_leaves_float_string_as_is(x):
    assume(not x.is_integer())
    assert fast_int(repr(x)) == repr(x)


def test_fast_int_converts_int_string_to_int_example():
    assert fast_int('-45') == -45
    assert fast_int('+45') == 45


@given(int)
def test_fast_int_converts_int_string_to_int(x):
    assert fast_int(repr(x)) == x


def test_fast_int_leaves_string_as_is_example():
    assert fast_int('invalid') == 'invalid'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(py23_str)
def test_fast_int_leaves_string_as_is(x):
    assume(not is_int(x))
    assert fast_int(x) == x


def test_isfloat_returns_True_for_real_numbers_example():
    assert isfloat(-45.0)
    assert isfloat(45.8e-2)


@given(float)
def test_isfloat_returns_True_for_real_numbers(x):
    assert isfloat(x)


def test_isfloat_returns_False_for_strings_example():
    assert not isfloat('45.8')
    assert not isfloat('invalid')


@given(py23_str)
def test_isfloat_returns_False_for_strings(x):
    assert not isfloat(x)


def test_isint_returns_True_for_real_numbers_example():
    assert isint(-45)
    assert isint(45)


@given(int)
def test_isint_returns_True_for_real_numbers(x):
    assert isint(x)


def test_isint_returns_False_for_strings_example():
    assert not isint('45')
    assert not isint('invalid')


@given(py23_str)
def test_isint_returns_False_for_strings(x):
    assert not isint(x)
