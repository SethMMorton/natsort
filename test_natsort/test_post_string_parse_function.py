# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from math import isnan, isinf
from natsort.ns_enum import ns
from natsort.utils import _post_string_parse_function
from natsort.compat.py23 import py23_str
from compat.hypothesis import (
    assume,
    given,
    text,
    floats,
    integers,
    use_hypothesis,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_post_string_parse_function_with_iterable_returns_tuple_with_no_options_example():
    assert _post_string_parse_function(0, '')(iter([7]), '') == (7, )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_string_parse_function_with_iterable_returns_tuple_with_no_options(x):
    assert _post_string_parse_function(0, '')(iter([x]), '') == (x, )
    # UNGROUPLETTERS without LOCALE does nothing, as does LOCALE without UNGROUPLETTERS
    assert _post_string_parse_function(ns.UNGROUPLETTERS, '')(iter([x]), '') == _post_string_parse_function(0, '')(iter([x]), '')
    assert _post_string_parse_function(ns.LOCALE, '')(iter([x]), '') == _post_string_parse_function(0, '')(iter([x]), '')


def test_post_string_parse_function_with_empty_tuple_returns_double_empty_tuple():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')((), '') == ((), ())


def test_post_string_parse_function_with_null_string_first_element_adds_empty_string_on_first_tuple_element():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')(('', 60), '') == (('',), ('', 60))


def test_post_string_parse_function_returns_first_element_in_first_tuple_element_example():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')(('this', 60), 'this60') == (('t',), ('this', 60))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(x=text(), y=floats() | integers())
def test_post_string_parse_function_returns_first_element_in_first_tuple_element(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')((x, y), ''.join(map(py23_str, [x, y]))) == ((x[0],), (x, y))


def test_post_string_parse_function_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST_example():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS | ns._DUMB | ns.LOWERCASEFIRST, '')(('this', 60), 'this60') == (('T',), ('this', 60))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(x=text(), y=floats() | integers())
def test_post_string_parse_function_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS | ns._DUMB | ns.LOWERCASEFIRST, '')((x, y), ''.join(map(py23_str, [x, y]))) == ((x[0].swapcase(),), (x, y))
