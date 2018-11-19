# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from hypothesis import example, given
from hypothesis.strategies import floats, integers, text
from natsort.compat.py23 import py23_str
from natsort.ns_enum import ns, ns_DUMB
from natsort.utils import final_data_transform_factory


@pytest.mark.parametrize("alg", [ns.DEFAULT, ns.UNGROUPLETTERS, ns.LOCALE])
@given(x=text(), y=floats(allow_nan=False, allow_infinity=False) | integers())
@pytest.mark.usefixtures("with_locale_en_us")
def test_final_data_transform_factory_default(x, y, alg):
    final_data_transform_func = final_data_transform_factory(alg, "", "::")
    value = (x, y)
    original_value = "".join(map(py23_str, value))
    result = final_data_transform_func(value, original_value)
    assert result == value


@pytest.mark.parametrize(
    "alg, func",
    [
        (ns.UNGROUPLETTERS | ns.LOCALE, lambda x: x),
        (ns.LOCALE | ns.UNGROUPLETTERS | ns_DUMB, lambda x: x),
        (ns.LOCALE | ns.UNGROUPLETTERS | ns.LOWERCASEFIRST, lambda x: x),
        (
            ns.LOCALE | ns.UNGROUPLETTERS | ns_DUMB | ns.LOWERCASEFIRST,
            lambda x: x.swapcase(),
        ),
    ],
)
@given(x=text(), y=floats(allow_nan=False, allow_infinity=False) | integers())
@example(x="İ", y=0)
@pytest.mark.usefixtures("with_locale_en_us")
def test_final_data_transform_factory_ungroup_and_locale(x, y, alg, func):
    final_data_transform_func = final_data_transform_factory(alg, "", "::")
    value = (x, y)
    original_value = "".join(map(py23_str, value))
    result = final_data_transform_func(value, original_value)
    if x:
        expected = ((func(original_value[:1]),), value)
    else:
        expected = (("::",), value)
    assert result == expected


def test_final_data_transform_factory_ungroup_and_locale_empty_tuple():
    final_data_transform_func = final_data_transform_factory(ns.UG | ns.L, "", "::")
    assert final_data_transform_func((), "") == ((), ())
