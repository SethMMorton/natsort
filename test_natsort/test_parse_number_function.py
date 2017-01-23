# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from math import isnan
from natsort.ns_enum import ns
from natsort.utils import _parse_number_factory
from compat.hypothesis import (
    assume,
    given,
    floats,
    integers,
    use_hypothesis,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_parse_number_factory_makes_function_that_returns_tuple_example():
    assert _parse_number_factory(0, '')(57) == ('', 57)
    assert _parse_number_factory(0, '')(float('nan')) == ('', float('-inf'))
    assert _parse_number_factory(ns.NANLAST, '')(float('nan')) == ('', float('+inf'))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test_parse_number_factory_makes_function_that_returns_tuple(x):
    assume(not isnan(x))
    assert _parse_number_factory(0, '')(x) == ('', x)


def test_parse_number_factory_with_PATH_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_factory(ns.PATH, '')(57) == (('', 57),)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test_parse_number_factory_with_PATH_makes_function_that_returns_nested_tuple(x):
    assume(not isnan(x))
    assert _parse_number_factory(ns.PATH, '')(x) == (('', x),)


def test_parse_number_factory_with_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_factory(ns.UNGROUPLETTERS | ns.LOCALE, '')(57) == (('',), ('', 57))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test_parse_number_factory_with_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple(x):
    assume(not isnan(x))
    assert _parse_number_factory(ns.UNGROUPLETTERS | ns.LOCALE, '')(x) == (('',), ('', x))


def test_parse_number_factory_with_PATH_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_factory(ns.PATH | ns.UNGROUPLETTERS | ns.LOCALE, '')(57) == ((('',), ('', 57)),)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test_parse_number_factory_with_PATH_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple(x):
    assume(not isnan(x))
    assert _parse_number_factory(ns.PATH | ns.UNGROUPLETTERS | ns.LOCALE, '')(x) == ((('',), ('', x)),)
