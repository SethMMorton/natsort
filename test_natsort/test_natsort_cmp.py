# -*- coding: utf-8 -*-
# pylint: disable=unused-variable
"""These test the natcmp() function.

Note that these tests are only relevant for Python version < 3.
"""
import sys
from functools import partial
from compat.mock import patch

import pytest
from hypothesis import given
from hypothesis.strategies import floats, integers, lists

from natsort import ns

from natsort.compat.py23 import py23_cmp

PY_VERSION = float(sys.version[:3])

if PY_VERSION < 3:
    from natsort import natcmp


class Comparable(object):
    """Stub class for testing natcmp functionality."""
    def __init__(self, value):
        self.value = value

    def __cmp__(self, other):
        return natcmp(self.value, other.value)


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
def test__classes_can_be_compared():
    one = Comparable("1")
    two = Comparable("2")
    another_two = Comparable("2")
    ten = Comparable("10")

    assert ten > two == another_two > one


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
def test__keys_are_being_cached():
    natcmp.cached_keys = {}
    assert len(natcmp.cached_keys) == 0
    natcmp(0, 0)
    assert len(natcmp.cached_keys) == 1
    natcmp(0, 0)
    assert len(natcmp.cached_keys) == 1

    with patch('natsort.compat.locale.dumb_sort', return_value=False):
        natcmp(0, 0, alg=ns.L)
        assert len(natcmp.cached_keys) == 2
        natcmp(0, 0, alg=ns.L)
        assert len(natcmp.cached_keys) == 2

    with patch('natsort.compat.locale.dumb_sort', return_value=True):
        natcmp(0, 0, alg=ns.L)
        assert len(natcmp.cached_keys) == 3
        natcmp(0, 0, alg=ns.L)
        assert len(natcmp.cached_keys) == 3


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
def test__illegal_algorithm_raises_error():
    try:
        natcmp(0, 0, alg="Just random stuff")
        assert False

    except ValueError:
        assert True

    except Exception:
        assert False


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
def test__classes_can_utilize_max_or_min():
    comparables = [Comparable(i) for i in range(10)]

    assert max(comparables) == comparables[-1]
    assert min(comparables) == comparables[0]


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
@given(integers(), integers())
def test__natcmp_works_the_same_for_integers_as_cmp(x, y):
    assert py23_cmp(x, y) == natcmp(x, y)


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
@given(floats(allow_nan=False), floats(allow_nan=False))
def test__natcmp_works_the_same_for_floats_as_cmp(x, y):
    assert py23_cmp(x, y) == natcmp(x, y)


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
@given(lists(elements=integers()))
def test_sort_strings_with_numbers(a_list):
    strings = [str(var) for var in a_list]
    natcmp_sorted = sorted(strings, cmp=partial(natcmp, alg=ns.SIGNED))

    assert sorted(a_list) == [int(var) for var in natcmp_sorted]
