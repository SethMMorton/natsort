# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from hypothesis import given
from hypothesis.strategies import floats, integers, text
from natsort.compat.py23 import py23_str
from natsort.ns_enum import ns, ns_DUMB
from natsort.utils import final_data_transform_factory

# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_final_data_transform_factory_with_iterable_returns_tuple_with_no_options_example():
    assert final_data_transform_factory(0, "", "")(iter([7]), "") == (7,)


@given(text())
def test_final_data_transform_factory_with_iterable_returns_tuple_with_no_options(x):
    assert final_data_transform_factory(0, "", "")(iter([x]), "") == (x,)
    # UNGROUPLETTERS without LOCALE does nothing, as does LOCALE without UNGROUPLETTERS
    assert final_data_transform_factory(ns.UNGROUPLETTERS, "", "")(
        iter([x]), ""
    ) == final_data_transform_factory(0, "", "")(iter([x]), "")
    assert final_data_transform_factory(ns.LOCALE, "", "")(
        iter([x]), ""
    ) == final_data_transform_factory(0, "", "")(iter([x]), "")


def test_final_data_transform_factory_with_empty_tuple_returns_double_empty_tuple():
    assert final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, "", "")(
        (), ""
    ) == ((), ())


def test_final_data_transform_factory_with_null_string_first_element_adds_empty_string_on_first_tuple_element():
    assert final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, "", "xx")(
        ("", 60), ""
    ) == (("xx",), ("", 60))


def test_final_data_transform_factory_returns_first_element_in_first_tuple_element_example():
    assert final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, "", "")(
        ("this", 60), "this60"
    ) == (("t",), ("this", 60))


@given(
    x=text().filter(bool), y=floats(allow_nan=False, allow_infinity=False) | integers()
)
def test_final_data_transform_factory_returns_first_element_in_first_tuple_element(
    x, y
):
    assert final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, "", "")(
        (x, y), "".join(map(py23_str, [x, y]))
    ) == ((x[0],), (x, y))


def test_final_data_transform_factory_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST_example():
    assert final_data_transform_factory(
        ns.LOCALE | ns.UNGROUPLETTERS | ns_DUMB | ns.LOWERCASEFIRST, "", ""
    )(("this", 60), "this60") == (("T",), ("this", 60))


@given(
    x=text().filter(bool), y=floats(allow_nan=False, allow_infinity=False) | integers()
)
def test_final_data_transform_factory_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST(
    x, y
):
    assert final_data_transform_factory(
        ns.LOCALE | ns.UNGROUPLETTERS | ns_DUMB | ns.LOWERCASEFIRST, "", ""
    )((x, y), "".join(map(py23_str, [x, y]))) == ((x[0].swapcase(),), (x, y))
