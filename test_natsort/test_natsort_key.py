# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from math import isnan
from natsort.compat.py23 import PY_VERSION
from natsort.ns_enum import ns
from natsort.utils import (
    _natsort_key,
    _regex_chooser,
    _parse_string_function,
    _parse_path_function,
    _parse_number_function,
    _parse_bytes_function,
    _pre_split_function,
    _post_split_function,
    _post_string_parse_function,
)
from compat.hypothesis import (
    assume,
    given,
    lists,
    text,
    floats,
    integers,
    binary,
    use_hypothesis,
)

if PY_VERSION >= 3:
    long = int


regex = _regex_chooser[ns.INT]
pre = _pre_split_function(ns.INT)
post = _post_split_function(ns.INT)
after = _post_string_parse_function(ns.INT, '')
string_func = _parse_string_function(ns.INT, '', regex.split, pre, post, after)
bytes_func = _parse_bytes_function(ns.INT)
num_func = _parse_number_function(ns.INT, '')


def test__natsort_key_with_numeric_input_and_PATH_returns_number_in_nested_tuple():
    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    sfunc = _parse_path_function(string_func)
    bytes_func = _parse_bytes_function(ns.PATH)
    num_func = _parse_number_function(ns.PATH, '')
    assert _natsort_key(10, None, sfunc, bytes_func, num_func) == (('', 10),)


@pytest.mark.skipif(PY_VERSION < 3, reason='only valid on python3')
def test__natsort_key_with_bytes_input_and_PATH_returns_number_in_nested_tuple():
    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    sfunc = _parse_path_function(string_func)
    bytes_func = _parse_bytes_function(ns.PATH)
    num_func = _parse_number_function(ns.PATH, '')
    assert _natsort_key(b'/hello/world', None, sfunc, bytes_func, num_func) == ((b'/hello/world',),)


def test__natsort_key_with_tuple_of_paths_and_PATH_returns_triply_nested_tuple():
    # PATH also handles recursion well.
    sfunc = _parse_path_function(string_func)
    bytes_func = _parse_bytes_function(ns.PATH)
    num_func = _parse_number_function(ns.PATH, '')
    assert _natsort_key(('/Folder', '/Folder (1)'), None, sfunc, bytes_func, num_func) == ((('/',), ('Folder',)), (('/',), ('Folder (', 1, ')')))


# The remaining tests provide no examples, just hypothesis tests.
# They only confirm that _natsort_key uses the above building blocks.


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test__natsort_key_with_numeric_input_takes_number_path(x):
    assume(not isnan(x))
    assert _natsort_key(x, None, string_func, bytes_func, num_func) == num_func(x)


@pytest.mark.skipif(PY_VERSION < 3, reason='only valid on python3')
@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(binary())
def test__natsort_key_with_bytes_input_takes_bytes_path(x):
    assume(x)
    assert _natsort_key(x, None, string_func, bytes_func, num_func) == bytes_func(x)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_text_input_takes_string_path(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, string_func, bytes_func, num_func) == string_func(s)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=text(), min_size=1, max_size=10))
def test__natsort_key_with_nested_input_takes_nested_path(x):
    assert _natsort_key(x, None, string_func, bytes_func, num_func) == tuple(string_func(s) for s in x)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test__natsort_key_with_key_argument_applies_key_before_processing(x):
    assert _natsort_key(x, len, string_func, bytes_func, num_func) == num_func(len(x))
