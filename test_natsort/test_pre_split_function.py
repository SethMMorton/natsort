# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
import locale
from operator import methodcaller
from natsort.ns_enum import ns
from natsort.utils import _pre_split_function
from natsort.compat.py23 import NEWPY
from compat.locale import (
    load_locale,
    has_locale_de_DE,
)
from compat.hypothesis import (
    given,
    text,
    integers,
    lists,
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


def test_pre_split_function_removes_thousands_separator_with_LOCALE_example():
    load_locale('en_US')
    x = '12,543,642,642.534,534,980'  # Without FLOAT it does not account for decimal.
    assert _pre_split_function(ns.LOCALE)(x) == '12543642642.534534980'
    x = '12,543,642,642.534,534,980'  # LOCALEALPHA doesn't do anything... need LOCALENUM
    assert _pre_split_function(ns.LOCALEALPHA)(x) == '12,543,642,642.534,534,980'
    locale.setlocale(locale.LC_ALL, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=integers(), min_size=4, max_size=20))
def test_pre_split_function_removes_thousands_separator_with_LOCALE(x):
    load_locale('en_US')
    t = ''.join(map(methodcaller('rstrip', 'lL'), map(str, map(abs, x))))  # Remove negative signs trailing L
    s = ''
    for i, y in enumerate(reversed(t), 1):
        s = y + s
        if i % 3 == 0 and i != len(t):
            s = ',' + s
    assert _pre_split_function(ns.LOCALE)(s) == t
    locale.setlocale(locale.LC_ALL, str(''))


def test_pre_split_function_removes_thousands_separator_and_is_float_aware_with_LOCALE_and_FLOAT_example():
    x = '12,543,642,642.534,534,980'
    assert _pre_split_function(ns.LOCALE | ns.FLOAT)(x) == '12543642642.534,534980'


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=integers(), min_size=4, max_size=20), lists(elements=integers(), min_size=4, max_size=20))
def test_pre_split_function_removes_thousands_separator_and_is_float_aware_with_LOCALE_and_FLOAT(x, y):
    load_locale('en_US')
    t = ''.join(map(methodcaller('rstrip', 'lL'), map(str, map(abs, x))))  # Remove negative signs trailing L
    s = ''
    for i, z in enumerate(reversed(t), 1):
        s = z + s
        if i % 3 == 0 and i != len(t):
            s = ',' + s
    u = ''.join(map(methodcaller('rstrip', 'lL'), map(str, map(abs, y))))  # Remove negative signs trailing L
    v = ''
    for i, z in enumerate(reversed(u), 1):
        v = z + v
        if i % 3 == 0 and i != len(u):
            v = ',' + v
    # Remove all but first comma.
    a = v.split(',', 1)
    p = a[0] + ',' + a[1].replace(',', '')
    assert _pre_split_function(ns.LOCALE)('.'.join([s, v])) == '.'.join([t, u])
    assert _pre_split_function(ns.LOCALE | ns.FLOAT)('.'.join([s, v])) == '.'.join([t, p])
    locale.setlocale(locale.LC_ALL, str(''))


# These might be too much to test with hypothesis.


def test_pre_split_function_leaves_invalid_thousands_separator_with_LOCALE_example():
    load_locale('en_US')
    x = '12,543,642642.5345,34980'
    assert _pre_split_function(ns.LOCALE)(x) == '12543,642642.5345,34980'
    x = '12,59443,642,642.53,4534980'
    assert _pre_split_function(ns.LOCALE)(x) == '12,59443,642642.53,4534980'
    x = '12543,642,642.5,34534980'
    assert _pre_split_function(ns.LOCALE)(x) == '12543,642642.5,34534980'
    locale.setlocale(locale.LC_ALL, str(''))


# @pytest.mark.skipif(not has_locale_de_DE or dumb_sort(), reason='requires de_DE locale and working locale')
@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale and working locale')
def test_pre_split_function_replaces_decimal_separator_with_LOCALE_example():
    load_locale('de_DE')
    x = '1543,753'
    assert _pre_split_function(ns.LOCALE)(x) == '1543,753'  # Does nothing without FLOAT
    assert _pre_split_function(ns.LOCALE | ns.FLOAT)(x) == '1543.753'
    assert _pre_split_function(ns.LOCALEALPHA)(x) == '1543,753'  # LOCALEALPHA doesn't do anything... need LOCALENUM
    locale.setlocale(locale.LC_ALL, str(''))


# @pytest.mark.skipif(not has_locale_de_DE or dumb_sort(), reason='requires de_DE locale and working locale')
@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale and working locale')
def test_pre_split_function_does_not_replace_invalid_decimal_separator_with_LOCALE_example():
    load_locale('de_DE')
    x = '154s,t53'
    assert _pre_split_function(ns.LOCALE | ns.FLOAT)(x) == '154s,t53'
    locale.setlocale(locale.LC_ALL, str(''))
