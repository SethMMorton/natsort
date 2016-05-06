# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import unicode_literals, print_function

import warnings
import locale
from pytest import raises
from natsort import (
    natsorted,
    natsort_key,
    natsort_keygen,
    ns,
)
from natsort.compat.py23 import PY_VERSION
from natsort.compat.locale import (
    null_string,
    get_strxfrm,
)
from compat.mock import patch
from compat.locale import load_locale

INPUT = ['6A-5.034e+1', '/Folder (1)/Foo', 56.7]


def test_natsort_key_public_raises_DeprecationWarning_when_called():
    # But it raises a deprecation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert natsort_key('a-5.034e2') == ('a-', 5, '.', 34, 'e', 2)
        assert len(w) == 1
        assert "natsort_key is deprecated as of 3.4.0, please use natsort_keygen" in str(w[-1].message)
    # It is called for each element in a list when sorting
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
        a.sort(key=natsort_key)
        assert len(w) == 7


def test_natsort_keygen_with_invalid_alg_input_raises_ValueError():
    # Invalid arguments give the correct response
    with raises(ValueError) as err:
        natsort_keygen(None, '1')
    assert str(err.value) == "natsort_keygen: 'alg' argument must be from the enum 'ns', got 1"


def test_natsort_keygen_returns_natsort_key_that_parses_input():
    a = 'a-5.034e1'
    assert natsort_keygen()(a) == ('a-', 5, '.', 34, 'e', 1)
    assert natsort_keygen(alg=ns.F | ns.S)(a) == ('a', -50.34)


def test_natsort_keygen_returns_key_that_can_be_used_to_sort_list_in_place_with_same_result_as_natsorted():
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    b = a[:]
    a.sort(key=natsort_keygen(alg=ns.F))
    assert a == natsorted(b, alg=ns.F)


def test_natsort_keygen_splits_input_with_defaults():
    assert natsort_keygen()(INPUT) == (('', 6, 'A-', 5, '.', 34, 'e+', 1), ('/Folder (', 1, ')/Foo'), ('', 56.7))
    if PY_VERSION >= 3: assert natsort_keygen()(b'6A-5.034e+1') == (b'6A-5.034e+1',)


def test_natsort_keygen_splits_input_with_real():
    assert natsort_keygen(alg=ns.R)(INPUT) == (('', 6.0, 'A', -50.34), ('/Folder (', 1.0, ')/Foo'), ('', 56.7))
    if PY_VERSION >= 3: assert natsort_keygen(alg=ns.R)(b'6A-5.034e+1') == (b'6A-5.034e+1',)


def test_natsort_keygen_splits_input_with_lowercasefirst_noexp_float():
    assert natsort_keygen(alg=ns.LF | ns.F | ns.N)(INPUT) == (('', 6.0, 'a-', 5.034, 'E+', 1.0), ('/fOLDER (', 1.0, ')/fOO'), ('', 56.7))
    if PY_VERSION >= 3: assert natsort_keygen(alg=ns.LF | ns.F | ns.N)(b'6A-5.034e+1') == (b'6A-5.034e+1',)


def test_natsort_keygen_splits_input_with_locale():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    with patch('natsort.compat.locale.dumb_sort', return_value=False):
        assert natsort_keygen(alg=ns.L)(INPUT) == ((null_string, 6, strxfrm('A-'), 5, strxfrm('.'), 34, strxfrm('e+'), 1), (strxfrm('/Folder ('), 1, strxfrm(')/Foo')), (null_string, 56.7))
    with patch('natsort.compat.locale.dumb_sort', return_value=True):
        assert natsort_keygen(alg=ns.L)(INPUT) == ((null_string, 6, strxfrm('aa--'), 5, strxfrm('..'), 34, strxfrm('eE++'), 1), (strxfrm('//ffoOlLdDeErR  (('), 1, strxfrm('))//ffoOoO')), (null_string, 56.7))
    if PY_VERSION >= 3: assert natsort_keygen(alg=ns.LA)(b'6A-5.034e+1') == (b'6A-5.034e+1',)
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsort_keygen_splits_input_with_locale_and_capitalfirst():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    with patch('natsort.compat.locale.dumb_sort', return_value=False):
        assert natsort_keygen(alg=ns.LA | ns.C)(INPUT) == ((('',), (null_string, 6, strxfrm('A-'), 5, strxfrm('.'), 34, strxfrm('e+'), 1)), (('/',), (strxfrm('/Folder ('), 1, strxfrm(')/Foo'))), (('',), (null_string, 56.7)))
    if PY_VERSION >= 3: assert natsort_keygen(alg=ns.LA | ns.C)(b'6A-5.034e+1') == (b'6A-5.034e+1',)
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsort_keygen_splits_input_with_path():
    assert natsort_keygen(alg=ns.P | ns.G)(INPUT) == ((('', 6, 'aA--', 5, '..', 34, 'ee++', 1),), (('//',), ('fFoollddeerr  ((', 1, '))'), ('fFoooo',)), (('', 56.7),))
    if PY_VERSION >= 3: assert natsort_keygen(alg=ns.P | ns.G)(b'6A-5.034e+1') == ((b'6A-5.034e+1',),)


def test_natsort_keygen_splits_input_with_ignorecase():
    assert natsort_keygen(alg=ns.IC)(INPUT) == (('', 6, 'a-', 5, '.', 34, 'e+', 1), ('/folder (', 1, ')/foo'), ('', 56.7))
    if PY_VERSION >= 3: assert natsort_keygen(alg=ns.IC)(b'6A-5.034e+1') == (b'6a-5.034e+1',)
