import sys
from functools import partial

import pytest
from hypothesis import given
from hypothesis.strategies import floats, integers, lists

from natsort import natcmp, ns

PY_VERSION = float(sys.version[:3])


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
def test__classes_can_be_compared():
    class Comparable:
        def __init__(self, value):
            self.value = value

        def __cmp__(self, other):
            return natcmp(self.value, other.value)

    one = Comparable("1")
    two = Comparable("2")
    another_two = Comparable("2")
    ten = Comparable("10")

    assert ten > two == another_two > one


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
def test__classes_can_utilize_max_or_min():
    class Comparable:
        def __init__(self, value):
            self.value = value

        def __cmp__(self, other):
            return natcmp(self.value, other.value)

    comparables = [Comparable(i) for i in range(10)]
    assert max(comparables) == comparables[-1]
    assert min(comparables) == comparables[0]


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
@given(integers(), integers())
def test__natcmp_works_the_same_for_integers_as_cmp(x, y):
    assert cmp(x, y) == natcmp(x, y)


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
@given(floats(allow_nan=False), floats(allow_nan=False))
def test__natcmp_works_the_same_for_floats_as_cmp(x, y):
    assert cmp(x, y) == natcmp(x, y)


@pytest.mark.skipif(PY_VERSION >= 3.0, reason='cmp() deprecated in Python 3')
@given(lists(elements=integers()))
def test_sort_strings_with_numbers(a_list):
    strings = map(str, a_list)
    natcmp_sorted = sorted(strings, cmp=partial(natcmp, alg=ns.REAL))

    assert sorted(a_list) == map(int, natcmp_sorted)
