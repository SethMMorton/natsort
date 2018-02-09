# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from natsort.ns_enum import ns
from natsort.utils import _parse_number_factory
from hypothesis import (
    given,
)
from hypothesis.strategies import (
    floats,
    integers,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_parse_number_factory_makes_function_that_returns_tuple_example():
    assert _parse_number_factory(0, '', '')(57) == ('', 57)
    assert _parse_number_factory(0, '', '')(float('nan')) == ('', float('-inf'))
    assert _parse_number_factory(ns.NANLAST, '', '')(float('nan')) == ('', float('+inf'))


@given(floats(allow_nan=False) | integers())
def test_parse_number_factory_makes_function_that_returns_tuple(x):
    assert _parse_number_factory(0, '', '')(x) == ('', x)


def test_parse_number_factory_with_PATH_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_factory(ns.PATH, '', '')(57) == (('', 57),)


@given(floats(allow_nan=False) | integers())
def test_parse_number_factory_with_PATH_makes_function_that_returns_nested_tuple(x):
    assert _parse_number_factory(ns.PATH, '', '')(x) == (('', x),)


def test_parse_number_factory_with_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_factory(ns.UNGROUPLETTERS | ns.LOCALE, '', 'xx')(57) == (('xx',), ('', 57))


@given(floats(allow_nan=False) | integers())
def test_parse_number_factory_with_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple(x):
    assert _parse_number_factory(ns.UNGROUPLETTERS | ns.LOCALE, '', 'xx')(x) == (('xx',), ('', x))


def test_parse_number_factory_with_PATH_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_factory(ns.PATH | ns.UNGROUPLETTERS | ns.LOCALE, '', 'xx')(57) == ((('xx',), ('', 57)),)


@given(floats(allow_nan=False) | integers())
def test_parse_number_factory_with_PATH_UNGROUPLETTERS_LOCALE_makes_function_that_returns_nested_tuple(x):
    assert _parse_number_factory(ns.PATH | ns.UNGROUPLETTERS | ns.LOCALE, '', 'xx')(x) == ((('xx',), ('', x)),)
