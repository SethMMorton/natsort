# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
from natsort.ns_enum import ns
from natsort.utils import _pre_split_function
from natsort.compat.py23 import NEWPY
from compat.hypothesis import (
    given,
    text,
    use_hypothesis,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_pre_split_function_is_no_op_for_no_alg_options_examples():
    x = 'feijGGAd'
    assert _pre_split_function(0)(x) is x


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_is_no_op_for_no_alg_options(x):
    assert _pre_split_function(0)(x) is x


def test_pre_split_function_performs_casefold_with_IGNORECASE_examples():
    x = 'feijGGAd'
    if NEWPY:
        assert _pre_split_function(ns.IGNORECASE)(x) == x.casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE)(x) == x.lower()


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_performs_casefold_with_IGNORECASE(x):
    if NEWPY:
        assert _pre_split_function(ns.IGNORECASE)(x) == x.casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE)(x) == x.lower()


def test_pre_split_function_performs_swapcase_with_DUMB_examples():
    x = 'feijGGAd'
    assert _pre_split_function(ns._DUMB)(x) == x.swapcase()


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_performs_swapcase_with_DUMB(x):
    assert _pre_split_function(ns._DUMB)(x) == x.swapcase()


def test_pre_split_function_performs_swapcase_with_LOWERCASEFIRST_example():
    x = 'feijGGAd'
    assert _pre_split_function(ns.LOWERCASEFIRST)(x) == x.swapcase()


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_performs_swapcase_with_LOWERCASEFIRST(x):
    x = 'feijGGAd'
    assert _pre_split_function(ns.LOWERCASEFIRST)(x) == x.swapcase()


def test_pre_split_function_is_no_op_with_both_LOWERCASEFIRST_AND_DUMB_example():
    x = 'feijGGAd'
    assert _pre_split_function(ns._DUMB | ns.LOWERCASEFIRST)(x) is x


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_is_no_op_with_both_LOWERCASEFIRST_AND_DUMB(x):
    assert _pre_split_function(ns._DUMB | ns.LOWERCASEFIRST)(x) is x


def test_pre_split_function_performs_swapcase_and_casefold_both_LOWERCASEFIRST_AND_IGNORECASE_example():
    x = 'feijGGAd'
    if NEWPY:
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().lower()


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_performs_swapcase_and_casefold_both_LOWERCASEFIRST_AND_IGNORECASE(x):
    if NEWPY:
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().lower()
