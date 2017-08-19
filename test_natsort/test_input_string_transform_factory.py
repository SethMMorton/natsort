# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pytest
import locale
from operator import methodcaller
from natsort.ns_enum import ns
from natsort.utils import _input_string_transform_factory
from natsort.compat.py23 import NEWPY
from compat.locale import (
    load_locale,
    has_locale_de_DE,
)
from hypothesis import (
    given,
)
from hypothesis.strategies import (
    text,
    integers,
    lists,
)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_input_string_transform_factory_is_no_op_for_no_alg_options_examples():
    x = 'feijGGAd'
    assert _input_string_transform_factory(0)(x) is x


@given(text())
def test_input_string_transform_factory_is_no_op_for_no_alg_options(x):
    assert _input_string_transform_factory(0)(x) is x


def test_input_string_transform_factory_performs_casefold_with_IGNORECASE_examples():
    x = 'feijGGAd'
    if NEWPY:
        assert _input_string_transform_factory(ns.IGNORECASE)(x) == x.casefold()
    else:
        assert _input_string_transform_factory(ns.IGNORECASE)(x) == x.lower()


@given(text())
def test_input_string_transform_factory_performs_casefold_with_IGNORECASE(x):
    if NEWPY:
        assert _input_string_transform_factory(ns.IGNORECASE)(x) == x.casefold()
    else:
        assert _input_string_transform_factory(ns.IGNORECASE)(x) == x.lower()


def test_input_string_transform_factory_performs_swapcase_with_DUMB_examples():
    x = 'feijGGAd'
    assert _input_string_transform_factory(ns._DUMB)(x) == x.swapcase()


@given(text())
def test_input_string_transform_factory_performs_swapcase_with_DUMB(x):
    assert _input_string_transform_factory(ns._DUMB)(x) == x.swapcase()


def test_input_string_transform_factory_performs_swapcase_with_LOWERCASEFIRST_example():
    x = 'feijGGAd'
    assert _input_string_transform_factory(ns.LOWERCASEFIRST)(x) == x.swapcase()


@given(text())
def test_input_string_transform_factory_performs_swapcase_with_LOWERCASEFIRST(x):
    x = 'feijGGAd'
    assert _input_string_transform_factory(ns.LOWERCASEFIRST)(x) == x.swapcase()


def test_input_string_transform_factory_is_no_op_with_both_LOWERCASEFIRST_AND_DUMB_example():
    x = 'feijGGAd'
    assert _input_string_transform_factory(ns._DUMB | ns.LOWERCASEFIRST)(x) is x


@given(text())
def test_input_string_transform_factory_is_no_op_with_both_LOWERCASEFIRST_AND_DUMB(x):
    assert _input_string_transform_factory(ns._DUMB | ns.LOWERCASEFIRST)(x) is x


def test_input_string_transform_factory_performs_swapcase_and_casefold_both_LOWERCASEFIRST_AND_IGNORECASE_example():
    x = 'feijGGAd'
    if NEWPY:
        assert _input_string_transform_factory(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().casefold()
    else:
        assert _input_string_transform_factory(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().lower()


@given(text())
def test_input_string_transform_factory_performs_swapcase_and_casefold_both_LOWERCASEFIRST_AND_IGNORECASE(x):
    if NEWPY:
        assert _input_string_transform_factory(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().casefold()
    else:
        assert _input_string_transform_factory(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().lower()


def test_input_string_transform_factory_removes_thousands_separator_with_LOCALE_example():
    load_locale('en_US')
    x = '12,543,642,642.534,534,980'  # Without FLOAT it does not account for decimal.
    assert _input_string_transform_factory(ns.LOCALE)(x) == '12543642642.534534980'
    x = '12,543,642,642.534,534,980'  # LOCALEALPHA doesn't do anything... need LOCALENUM
    assert _input_string_transform_factory(ns.LOCALEALPHA)(x) == '12,543,642,642.534,534,980'
    locale.setlocale(locale.LC_ALL, str(''))


@given(lists(elements=integers(), min_size=4, max_size=20))
def test_input_string_transform_factory_removes_thousands_separator_with_LOCALE(x):
    load_locale('en_US')
    t = ''.join(map(methodcaller('rstrip', 'lL'), map(str, map(abs, x))))  # Remove negative signs trailing L
    s = ''
    for i, y in enumerate(reversed(t), 1):
        s = y + s
        if i % 3 == 0 and i != len(t):
            s = ',' + s
    assert _input_string_transform_factory(ns.LOCALE)(s) == t
    locale.setlocale(locale.LC_ALL, str(''))


def test_input_string_transform_factory_removes_thousands_separator_and_is_float_aware_with_LOCALE_and_FLOAT_example():
    x = '12,543,642,642.534,534,980'
    assert _input_string_transform_factory(ns.LOCALE | ns.FLOAT)(x) == '12543642642.534,534980'


@given(lists(elements=integers(), min_size=4, max_size=20), lists(elements=integers(), min_size=4, max_size=20))
def test_input_string_transform_factory_removes_thousands_separator_and_is_float_aware_with_LOCALE_and_FLOAT(x, y):
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
    assert _input_string_transform_factory(ns.LOCALE)('.'.join([s, v])) == '.'.join([t, u])
    assert _input_string_transform_factory(ns.LOCALE | ns.FLOAT)('.'.join([s, v])) == '.'.join([t, p])
    locale.setlocale(locale.LC_ALL, str(''))


# These might be too much to test with hypothesis.


def test_input_string_transform_factory_leaves_invalid_thousands_separator_with_LOCALE_example():
    load_locale('en_US')
    x = '12,543,642642.5345,34980'
    assert _input_string_transform_factory(ns.LOCALE)(x) == '12543,642642.5345,34980'
    x = '12,59443,642,642.53,4534980'
    assert _input_string_transform_factory(ns.LOCALE)(x) == '12,59443,642642.53,4534980'
    x = '12543,642,642.5,34534980'
    assert _input_string_transform_factory(ns.LOCALE)(x) == '12543,642642.5,34534980'
    locale.setlocale(locale.LC_ALL, str(''))


# @pytest.mark.skipif(not has_locale_de_DE or dumb_sort(), reason='requires de_DE locale and working locale')
@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale and working locale')
def test_input_string_transform_factory_replaces_decimal_separator_with_LOCALE_example():
    load_locale('de_DE')
    x = '1543,753'
    assert _input_string_transform_factory(ns.LOCALE)(x) == '1543,753'  # Does nothing without FLOAT
    assert _input_string_transform_factory(ns.LOCALE | ns.FLOAT)(x) == '1543.753'
    assert _input_string_transform_factory(ns.LOCALEALPHA)(x) == '1543,753'  # LOCALEALPHA doesn't do anything... need LOCALENUM
    locale.setlocale(locale.LC_ALL, str(''))


# @pytest.mark.skipif(not has_locale_de_DE or dumb_sort(), reason='requires de_DE locale and working locale')
@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale and working locale')
def test_input_string_transform_factory_does_not_replace_invalid_decimal_separator_with_LOCALE_example():
    load_locale('de_DE')
    x = '154s,t53'
    assert _input_string_transform_factory(ns.LOCALE | ns.FLOAT)(x) == '154s,t53'
    locale.setlocale(locale.LC_ALL, str(''))
