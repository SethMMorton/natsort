# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from hypothesis import given
from hypothesis.strategies import binary, floats, integers, lists, text
from natsort.compat.py23 import PY_VERSION, py23_str
from natsort.utils import natsort_key

if PY_VERSION >= 3:
    long = int


def str_func(x):
    if isinstance(x, py23_str):
        return x
    else:
        raise TypeError("Not a str!")


def fail(_):
    raise AssertionError("This should never be reached!")


@given(floats(allow_nan=False) | integers())
def test_natsort_key_with_numeric_input_takes_number_path(x):
    assert natsort_key(x, None, str_func, fail, lambda y: y) is x


@pytest.mark.skipif(PY_VERSION < 3, reason="only valid on python3")
@given(binary().filter(bool))
def test_natsort_key_with_bytes_input_takes_bytes_path(x):
    assert natsort_key(x, None, str_func, lambda y: y, fail) is x


@given(text())
def test_natsort_key_with_text_input_takes_string_path(x):
    assert natsort_key(x, None, str_func, fail, fail) is x


@given(lists(elements=text(), min_size=1, max_size=10))
def test_natsort_key_with_nested_input_takes_nested_path(x):
    assert natsort_key(x, None, str_func, fail, fail) == tuple(x)


@given(text())
def test_natsort_key_with_key_argument_applies_key_before_processing(x):
    assert natsort_key(x, len, str_func, fail, lambda y: y) == len(x)
