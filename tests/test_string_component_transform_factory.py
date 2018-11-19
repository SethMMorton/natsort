# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from functools import partial

import pytest
from hypothesis import example, given
from hypothesis.strategies import floats, integers, text
from natsort.compat.fastnumbers import fast_float, fast_int
from natsort.compat.locale import get_strxfrm
from natsort.compat.py23 import py23_range, py23_str, py23_unichr
from natsort.ns_enum import ns, ns_DUMB
from natsort.utils import groupletters, string_component_transform_factory

# There are some unicode values that are known failures with the builtin locale
# library on BSD systems that has nothing to do with natsort (a ValueError is
# raised by strxfrm). Let's filter them out.
try:
    bad_uni_chars = frozenset(
        py23_unichr(x) for x in py23_range(0X10fefd, 0X10ffff + 1)
    )
except ValueError:
    # Narrow unicode build... no worries.
    bad_uni_chars = frozenset()


def no_bad_uni_chars(x, _bad_chars=bad_uni_chars):
    """Ensure text does not contain bad unicode characters"""
    return not any(y in _bad_chars for y in x)


def no_null(x):
    """Ensure text does not contain a null character."""
    return "\0" not in x


@pytest.mark.parametrize(
    "alg, example_func",
    [
        (ns.INT, fast_int),
        (ns.DEFAULT, fast_int),
        (ns.FLOAT, partial(fast_float, nan=float("-inf"))),
        (ns.FLOAT | ns.NANLAST, partial(fast_float, nan=float("+inf"))),
        (ns.GROUPLETTERS, partial(fast_int, key=groupletters)),
        (ns.LOCALE, partial(fast_int, key=lambda x: get_strxfrm()(x))),
        (
            ns.GROUPLETTERS | ns.LOCALE,
            partial(fast_int, key=lambda x: get_strxfrm()(groupletters(x))),
        ),
        (
            ns_DUMB | ns.LOCALE,
            partial(fast_int, key=lambda x: get_strxfrm()(groupletters(x))),
        ),
        (
            ns.GROUPLETTERS | ns.LOCALE | ns.FLOAT | ns.NANLAST,
            partial(
                fast_float,
                key=lambda x: get_strxfrm()(groupletters(x)),
                nan=float("+inf"),
            ),
        ),
    ],
)
@example(x=float("nan"))
@given(
    x=integers()
    | floats()
    | text().filter(bool).filter(no_bad_uni_chars).filter(no_null)
)
@pytest.mark.usefixtures("with_locale_en_us")
def test_string_component_transform_factory(x, alg, example_func):
    string_component_transform_func = string_component_transform_factory(alg)
    try:
        assert string_component_transform_func(py23_str(x)) == example_func(py23_str(x))
    except ValueError as e:  # handle broken locale lib on BSD.
        if "is not in range" not in str(e):
            raise
