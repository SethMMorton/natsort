# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from math import isnan, isinf
from natsort.ns_enum import ns
from natsort.utils import _final_data_transform_factory
from natsort.compat.py23 import py23_str
from hypothesis import (
    assume,
    given,
)
from hypothesis.strategies import (
    text,
    floats,
    integers,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_final_data_transform_factory_with_iterable_returns_tuple_with_no_options_example():
    assert _final_data_transform_factory(0, '')(iter([7]), '') == (7,)


@given(text())
def test_final_data_transform_factory_with_iterable_returns_tuple_with_no_options(x):
    assert _final_data_transform_factory(0, '')(iter([x]), '') == (x,)
    # UNGROUPLETTERS without LOCALE does nothing, as does LOCALE without UNGROUPLETTERS
    assert _final_data_transform_factory(ns.UNGROUPLETTERS, '')(iter([x]), '') == _final_data_transform_factory(0, '')(iter([x]), '')
    assert _final_data_transform_factory(ns.LOCALE, '')(iter([x]), '') == _final_data_transform_factory(0, '')(iter([x]), '')


def test_final_data_transform_factory_with_empty_tuple_returns_double_empty_tuple():
    assert _final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, '')((), '') == ((), ())


def test_final_data_transform_factory_with_null_string_first_element_adds_empty_string_on_first_tuple_element():
    assert _final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, '')(('', 60), '') == (('',), ('', 60))


def test_final_data_transform_factory_returns_first_element_in_first_tuple_element_example():
    assert _final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, '')(('this', 60), 'this60') == (('t',), ('this', 60))


@given(x=text(), y=floats() | integers())
def test_final_data_transform_factory_returns_first_element_in_first_tuple_element(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS, '')((x, y), ''.join(map(py23_str, [x, y]))) == ((x[0],), (x, y))


def test_final_data_transform_factory_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST_example():
    assert _final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS | ns._DUMB | ns.LOWERCASEFIRST, '')(('this', 60), 'this60') == (('T',), ('this', 60))


@given(x=text(), y=floats() | integers())
def test_final_data_transform_factory_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _final_data_transform_factory(ns.LOCALE | ns.UNGROUPLETTERS | ns._DUMB | ns.LOWERCASEFIRST, '')((x, y), ''.join(map(py23_str, [x, y]))) == ((x[0].swapcase(),), (x, y))
