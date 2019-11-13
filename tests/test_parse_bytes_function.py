# -*- coding: utf-8 -*-
"""These test the utils.py functions."""

import pytest
from hypothesis import given
from hypothesis.strategies import binary
from natsort.ns_enum import ns
from natsort.utils import parse_bytes_factory


@pytest.mark.parametrize(
    "alg, example_func",
    [
        (ns.DEFAULT, lambda x: (x,)),
        (ns.IGNORECASE, lambda x: (x.lower(),)),
        # With PATH, it becomes a tested tuple.
        (ns.PATH, lambda x: ((x,),)),
        (ns.PATH | ns.IGNORECASE, lambda x: ((x.lower(),),)),
    ],
)
@given(x=binary())
def test_parse_bytest_factory_makes_function_that_returns_tuple(x, alg, example_func):
    parse_bytes_func = parse_bytes_factory(alg)
    assert parse_bytes_func(x) == example_func(x)
