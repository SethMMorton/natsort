# -*- coding: utf-8 -*-
"""\
Test the fake fastnumbers module.
"""
from __future__ import unicode_literals

import unicodedata
from math import isnan
from natsort.compat.py23 import PY_VERSION
from natsort.compat.fake_fastnumbers import (
    fast_float,
    fast_int,
)
from hypothesis import (
    assume,
    given,
)
from hypothesis.strategies import (
    floats,
    integers,
    text,
)

if PY_VERSION >= 3:
    long = int


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
        long(x)
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


def test_fast_float_returns_nan_alternate_if_nan_option_is_given():
    assert fast_float('nan', nan=7) == 7


def test_fast_float_converts_float_string_to_float_example():
    assert fast_float('45.8') == 45.8
    assert fast_float('-45') == -45.0
    assert fast_float('45.8e-2', key=len) == 45.8e-2
    assert isnan(fast_float('nan'))
    assert isnan(fast_float('+nan'))
    assert isnan(fast_float('-NaN'))


@given(floats())
def test_fast_float_converts_float_string_to_float(x):
    assume(not isnan(x))  # But inf is included
    assert fast_float(repr(x)) == x


def test_fast_float_leaves_string_as_is_example():
    assert fast_float('invalid') == 'invalid'


@given(text())
def test_fast_float_leaves_string_as_is(x):
    assume(not is_float(x))
    assume(bool(x))
    assert fast_float(x) == x


def test_fast_float_with_key_applies_to_string_example():
    assert fast_float('invalid', key=len) == len('invalid')


@given(text())
def test_fast_float_with_key_applies_to_string(x):
    assume(not is_float(x))
    assume(bool(x))
    assert fast_float(x, key=len) == len(x)


def test_fast_int_leaves_float_string_as_is_example():
    assert fast_int('45.8') == '45.8'
    assert fast_int('nan') == 'nan'
    assert fast_int('inf') == 'inf'


@given(floats())
def test_fast_int_leaves_float_string_as_is(x):
    assume(not x.is_integer())
    assert fast_int(repr(x)) == repr(x)


def test_fast_int_converts_int_string_to_int_example():
    assert fast_int('-45') == -45
    assert fast_int('+45') == 45


@given(integers())
def test_fast_int_converts_int_string_to_int(x):
    assert fast_int(repr(x)) == x


def test_fast_int_leaves_string_as_is_example():
    assert fast_int('invalid') == 'invalid'


@given(text())
def test_fast_int_leaves_string_as_is(x):
    assume(not is_int(x))
    assume(bool(x))
    assert fast_int(x) == x


def test_fast_int_with_key_applies_to_string_example():
    assert fast_int('invalid', key=len) == len('invalid')


@given(text())
def test_fast_int_with_key_applies_to_string(x):
    assume(not is_int(x))
    assume(bool(x))
    assert fast_int(x, key=len) == len(x)
