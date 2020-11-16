# -*- coding: utf-8 -*-
"""These test the utils.py functions."""

import pytest
from hypothesis import given
from hypothesis.strategies import floats, integers
from natsort.ns_enum import ns
from natsort.utils import parse_number_or_none_factory


@pytest.mark.usefixtures("with_locale_en_us")
@pytest.mark.parametrize(
    "alg, example_func",
    [
        (ns.DEFAULT, lambda x: ("", x)),
        (ns.PATH, lambda x: (("", x),)),
        (ns.UNGROUPLETTERS | ns.LOCALE, lambda x: (("xx",), ("", x))),
        (ns.PATH | ns.UNGROUPLETTERS | ns.LOCALE, lambda x: ((("xx",), ("", x)),)),
    ],
)
@given(x=floats(allow_nan=False) | integers())
def test_parse_number_factory_makes_function_that_returns_tuple(x, alg, example_func):
    parse_number_func = parse_number_or_none_factory(alg, "", "xx")
    assert parse_number_func(x) == example_func(x)


@pytest.mark.parametrize(
    "alg, x, result",
    [
        (ns.DEFAULT, 57, ("", 57)),
        (ns.DEFAULT, float("nan"), ("", float("-inf"))),  # NaN transformed to -infinity
        (ns.NANLAST, float("nan"), ("", float("+inf"))),  # NANLAST makes it +infinity
        (ns.DEFAULT, None, ("", float("-inf"))),  # None transformed to -infinity
        (ns.NANLAST, None, ("", float("+inf"))),  # NANLAST makes it +infinity
    ],
)
def test_parse_number_factory_treats_nan_and_none_special(alg, x, result):
    parse_number_func = parse_number_or_none_factory(alg, "", "xx")
    assert parse_number_func(x) == result
