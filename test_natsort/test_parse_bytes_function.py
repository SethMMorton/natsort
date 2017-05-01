# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from natsort.ns_enum import ns
from natsort.utils import _parse_bytes_factory
from hypothesis import given
from hypothesis.strategies import binary


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_parse_bytes_factory_makes_function_that_returns_tuple_example():
    assert _parse_bytes_factory(0)(b'hello') == (b'hello',)


@given(binary())
def test_parse_bytes_factory_makes_function_that_returns_tuple(x):
    assert _parse_bytes_factory(0)(x) == (x,)


def test_parse_bytes_factory_with_IGNORECASE_makes_function_that_returns_tuple_with_lowercase_example():
    assert _parse_bytes_factory(ns.IGNORECASE)(b'HelLo') == (b'hello',)


@given(binary())
def test_parse_bytes_factory_with_IGNORECASE_makes_function_that_returns_tuple_with_lowercase(x):
    assert _parse_bytes_factory(ns.IGNORECASE)(x) == (x.lower(),)


def test_parse_bytes_factory_with_PATH_makes_function_that_returns_nested_tuple_example():
    assert _parse_bytes_factory(ns.PATH)(b'hello') == ((b'hello',),)


@given(binary())
def test_parse_bytes_factory_with_PATH_makes_function_that_returns_nested_tuple(x):
    assert _parse_bytes_factory(ns.PATH)(x) == ((x,),)


def test_parse_bytes_factory_with_PATH_and_IGNORECASE_makes_function_that_returns_nested_tuple_with_lowercase_example():
    assert _parse_bytes_factory(ns.PATH | ns.IGNORECASE)(b'HelLo') == ((b'hello',),)


@given(binary())
def test_parse_bytes_factory_with_PATH_and_IGNORECASE_makes_function_that_returns_nested_tuple_with_lowercase(x):
    assert _parse_bytes_factory(ns.PATH | ns.IGNORECASE)(x) == ((x.lower(),),)
