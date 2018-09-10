# -*- coding: utf-8 -*-
# pylint: disable=unused-variable
"""These test the natcmp() function.

Note that these tests are only relevant for Python version < 3.
"""
from functools import partial

import pytest
from hypothesis import given
from hypothesis.strategies import floats, integers, lists
from natsort import ns
from natsort.compat.py23 import PY_VERSION, py23_cmp

if PY_VERSION < 3:
    from natsort import natcmp


class Comparable(object):
    """Stub class for testing natcmp functionality."""

    def __init__(self, value):
        self.value = value

    def __cmp__(self, other):
        return natcmp(self.value, other.value)


@pytest.mark.skipif(PY_VERSION >= 3.0, reason="cmp() deprecated in Python 3")
class TestNatCmp:

    def test_classes_can_be_compared(self):
        one = Comparable("1")
        two = Comparable("2")
        another_two = Comparable("2")
        ten = Comparable("10")
        assert ten > two == another_two > one

    def test_keys_are_being_cached(self, mocker):
        natcmp.cached_keys = {}
        assert len(natcmp.cached_keys) == 0
        natcmp(0, 0)
        assert len(natcmp.cached_keys) == 1
        natcmp(0, 0)
        assert len(natcmp.cached_keys) == 1

        with mocker.patch("natsort.compat.locale.dumb_sort", return_value=False):
            natcmp(0, 0, alg=ns.L)
            assert len(natcmp.cached_keys) == 2
            natcmp(0, 0, alg=ns.L)
            assert len(natcmp.cached_keys) == 2

        with mocker.patch("natsort.compat.locale.dumb_sort", return_value=True):
            natcmp(0, 0, alg=ns.L)
            assert len(natcmp.cached_keys) == 3
            natcmp(0, 0, alg=ns.L)
            assert len(natcmp.cached_keys) == 3

    def test_illegal_algorithm_raises_error(self):
        with pytest.raises(ValueError):
            natcmp(0, 0, alg="Just random stuff")

    def test_classes_can_utilize_max_or_min(self):
        comparables = [Comparable(i) for i in range(10)]

        assert max(comparables) == comparables[-1]
        assert min(comparables) == comparables[0]

    @given(integers(), integers())
    def test_natcmp_works_the_same_for_integers_as_cmp(self, x, y):
        assert py23_cmp(x, y) == natcmp(x, y)

    @given(floats(allow_nan=False), floats(allow_nan=False))
    def test_natcmp_works_the_same_for_floats_as_cmp(self, x, y):
        assert py23_cmp(x, y) == natcmp(x, y)

    @given(lists(elements=integers()))
    def test_sort_strings_with_numbers(self, a_list):
        strings = [str(var) for var in a_list]
        # noinspection PyArgumentList
        natcmp_sorted = sorted(strings, cmp=partial(natcmp, alg=ns.SIGNED))

        assert sorted(a_list) == [int(var) for var in natcmp_sorted]
