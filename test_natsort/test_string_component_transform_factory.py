# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from natsort.ns_enum import ns
from natsort.utils import (
    _string_component_transform_factory,
    _groupletters,
)
from natsort.compat.py23 import py23_str
from natsort.compat.locale import get_strxfrm
from natsort.compat.fastnumbers import (
    fast_float,
    fast_int,
)
from hypothesis import (
    assume,
    given,
)
from hypothesis.strategies import (
    text,
    floats,
    integers,
)
from compat.locale import bad_uni_chars


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_string_component_transform_factory_returns_fast_int_example():
    x = 'hello'
    assert _string_component_transform_factory(0)(x) is fast_int(x)
    assert _string_component_transform_factory(0)('5007') == fast_int('5007')


@given(text() | floats() | integers())
def test_string_component_transform_factory_returns_fast_int(x):
    assume(x)
    assert _string_component_transform_factory(0)(py23_str(x)) == fast_int(py23_str(x))


def test_string_component_transform_factory_with_FLOAT_returns_fast_float_example():
    x = 'hello'
    assert _string_component_transform_factory(ns.FLOAT)(x) is fast_float(x)
    assert _string_component_transform_factory(ns.FLOAT)('5007') == fast_float('5007')


@given(text() | floats() | integers())
def test_string_component_transform_factory_with_FLOAT_returns_fast_float(x):
    assume(x)
    assert _string_component_transform_factory(ns.FLOAT)(py23_str(x)) == fast_float(py23_str(x), nan=float('-inf'))


def test_string_component_transform_factory_with_FLOAT_returns_fast_float_with_neg_inf_replacing_nan():
    assert _string_component_transform_factory(ns.FLOAT)('nan') == fast_float('nan', nan=float('-inf'))


def test_string_component_transform_factory_with_FLOAT_and_NANLAST_returns_fast_float_with_pos_inf_replacing_nan():
    assert _string_component_transform_factory(ns.FLOAT | ns.NANLAST)('nan') == fast_float('nan', nan=float('+inf'))


def test_string_component_transform_factory_with_GROUPLETTERS_returns_fast_int_and_groupletters_example():
    x = 'hello'
    assert _string_component_transform_factory(ns.GROUPLETTERS)(x) == fast_int(x, key=_groupletters)


@given(text())
def test_string_component_transform_factory_with_GROUPLETTERS_returns_fast_int_and_groupletters(x):
    assume(x)
    assert _string_component_transform_factory(ns.GROUPLETTERS)(x) == fast_int(x, key=_groupletters)


def test_string_component_transform_factory_with_LOCALE_returns_fast_int_and_groupletters_example():
    x = 'hello'
    assert _string_component_transform_factory(ns.LOCALE)(x) == fast_int(x, key=get_strxfrm())


@given(text())
def test_string_component_transform_factory_with_LOCALE_returns_fast_int_and_groupletters(x):
    assume(x)
    assume(not any(y in bad_uni_chars for y in x))
    assume('\0' not in x)
    assert _string_component_transform_factory(ns.LOCALE)(x) == fast_int(x, key=get_strxfrm())


def test_string_component_transform_factory_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _string_component_transform_factory(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))


@given(text())
def test_string_component_transform_factory_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    assume('\0' not in x)
    try:
        assert _string_component_transform_factory(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise


def test_string_component_transform_factory_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _string_component_transform_factory(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))


@given(text())
def test_string_component_transform_factory_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    assume('\0' not in x)
    try:
        assert _string_component_transform_factory(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: get_strxfrm()(_groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise
