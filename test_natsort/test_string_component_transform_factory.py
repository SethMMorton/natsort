# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from hypothesis import given
from hypothesis.strategies import floats, integers, text
from natsort.compat.fastnumbers import fast_float, fast_int
from natsort.compat.locale import get_strxfrm
from natsort.compat.py23 import py23_str, py23_unichr, py23_range
from natsort.ns_enum import ns, ns_DUMB
from natsort.utils import groupletters, string_component_transform_factory

# There are some unicode values that are known failures with the builtin locale
# library on BSD systems that has nothing to do with natsort (a ValueError is
# raised by strxfrm). Let's filter them out.
try:
    bad_uni_chars = set(py23_unichr(x) for x in py23_range(0X10fefd, 0X10ffff + 1))
except ValueError:
    # Narrow unicode build... no worries.
    bad_uni_chars = set()


def no_null(x):
    return "\0" not in x


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_string_component_transform_factory_returns_fast_int_example():
    x = "hello"
    assert string_component_transform_factory(0)(x) is fast_int(x)
    assert string_component_transform_factory(0)("5007") == fast_int("5007")


@given(text().filter(bool) | floats() | integers())
def test_string_component_transform_factory_returns_fast_int(x):
    assert string_component_transform_factory(0)(py23_str(x)) == fast_int(py23_str(x))


def test_string_component_transform_factory_with_FLOAT_returns_fast_float_example():
    x = "hello"
    assert string_component_transform_factory(ns.FLOAT)(x) is fast_float(x)
    assert string_component_transform_factory(ns.FLOAT)("5007") == fast_float("5007")


@given(text().filter(bool) | floats() | integers())
def test_string_component_transform_factory_with_FLOAT_returns_fast_float(x):
    assert string_component_transform_factory(ns.FLOAT)(py23_str(x)) == fast_float(
        py23_str(x), nan=float("-inf")
    )


def test_string_component_transform_factory_with_FLOAT_returns_fast_float_with_neg_inf_replacing_nan():
    assert string_component_transform_factory(ns.FLOAT)("nan") == fast_float(
        "nan", nan=float("-inf")
    )


def test_string_component_transform_factory_with_FLOAT_and_NANLAST_returns_fast_float_with_pos_inf_replacing_nan():
    assert string_component_transform_factory(ns.FLOAT | ns.NANLAST)(
        "nan"
    ) == fast_float("nan", nan=float("+inf"))


def test_string_component_transform_factory_with_GROUPLETTERS_returns_fast_int_and_groupletters_example():
    x = "hello"
    assert string_component_transform_factory(ns.GROUPLETTERS)(x) == fast_int(
        x, key=groupletters
    )


@given(text().filter(bool))
def test_string_component_transform_factory_with_GROUPLETTERS_returns_fast_int_and_groupletters(
    x
):
    assert string_component_transform_factory(ns.GROUPLETTERS)(x) == fast_int(
        x, key=groupletters
    )


def test_string_component_transform_factory_with_LOCALE_returns_fast_int_and_groupletters_example():
    x = "hello"
    assert string_component_transform_factory(ns.LOCALE)(x) == fast_int(
        x, key=get_strxfrm()
    )


@given(
    text()
    .filter(bool)
    .filter(lambda x: not any(y in bad_uni_chars for y in x))
    .filter(no_null)
)
def test_string_component_transform_factory_with_LOCALE_returns_fast_int_and_groupletters(
    x
):
    assert string_component_transform_factory(ns.LOCALE)(x) == fast_int(
        x, key=get_strxfrm()
    )


def test_string_component_transform_factory_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = "hello"
    assert string_component_transform_factory(ns.GROUPLETTERS | ns.LOCALE)(
        x
    ) == fast_int(x, key=lambda x: get_strxfrm()(groupletters(x)))


@given(text().filter(bool).filter(no_null))
def test_string_component_transform_factory_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert(
    x
):
    try:
        assert string_component_transform_factory(ns.GROUPLETTERS | ns.LOCALE)(
            x
        ) == fast_int(x, key=lambda x: get_strxfrm()(groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if "is not in range" not in str(e):
            raise


def test_string_component_transform_factory_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = "hello"
    assert string_component_transform_factory(ns_DUMB | ns.LOCALE)(x) == fast_int(
        x, key=lambda x: get_strxfrm()(groupletters(x))
    )


@given(text().filter(bool).filter(no_null))
def test_string_component_transform_factory_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert(
    x
):
    try:
        assert string_component_transform_factory(ns_DUMB | ns.LOCALE)(x) == fast_int(
            x, key=lambda x: get_strxfrm()(groupletters(x))
        )
    except ValueError as e:  # handle broken locale lib on BSD.
        if "is not in range" not in str(e):
            raise
