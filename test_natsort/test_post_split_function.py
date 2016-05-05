# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from natsort.ns_enum import ns
from natsort.utils import (
    _post_split_function,
    _groupletters,
)
from natsort.compat.py23 import py23_str
from natsort.compat.locale import get_strxfrm
from natsort.compat.fastnumbers import (
    fast_float,
    fast_int,
)
from compat.hypothesis import (
    assume,
    given,
    text,
    floats,
    integers,
    use_hypothesis,
)
from compat.locale import bad_uni_chars


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_post_split_function_returns_fast_int_example():
    x = 'hello'
    assert _post_split_function(0)(x) is fast_int(x)
    assert _post_split_function(0)('5007') == fast_int('5007')


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text() | floats() | integers())
def test_post_split_function_returns_fast_int(x):
    assume(x)
    assert _post_split_function(0)(py23_str(x)) == fast_int(py23_str(x))


def test_post_split_function_with_FLOAT_returns_fast_float_example():
    x = 'hello'
    assert _post_split_function(ns.FLOAT)(x) is fast_float(x)
    assert _post_split_function(ns.FLOAT)('5007') == fast_float('5007')


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text() | floats() | integers())
def test_post_split_function_with_FLOAT_returns_fast_float(x):
    assume(x)
    assert _post_split_function(ns.FLOAT)(py23_str(x)) == fast_float(py23_str(x), nan=float('-inf'))


def test_post_split_function_with_FLOAT_returns_fast_float_with_neg_inf_replacing_nan():
    assert _post_split_function(ns.FLOAT)('nan') == fast_float('nan', nan=float('-inf'))


def test_post_split_function_with_FLOAT_and_NANLAST_returns_fast_float_with_pos_inf_replacing_nan():
    assert _post_split_function(ns.FLOAT | ns.NANLAST)('nan') == fast_float('nan', nan=float('+inf'))


def test_post_split_function_with_GROUPLETTERS_returns_fast_int_and_groupletters_example():
    x = 'hello'
    assert _post_split_function(ns.GROUPLETTERS)(x) == fast_int(x, key=_groupletters)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_GROUPLETTERS_returns_fast_int_and_groupletters(x):
    assume(x)
    assert _post_split_function(ns.GROUPLETTERS)(x) == fast_int(x, key=_groupletters)


def test_post_split_function_with_LOCALE_returns_fast_int_and_groupletters_example():
    x = 'hello'
    assert _post_split_function(ns.LOCALE)(x) == fast_int(x, key=get_strxfrm())


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_returns_fast_int_and_groupletters(x):
    assume(x)
    assume(not any(y in bad_uni_chars for y in x))
    assert _post_split_function(ns.LOCALE)(x) == fast_int(x, key=get_strxfrm())


def test_post_split_function_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _post_split_function(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    try:
        assert _post_split_function(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise


def test_post_split_function_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _post_split_function(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    try:
        assert _post_split_function(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise
