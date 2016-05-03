# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import unicode_literals, print_function
import warnings
from pytest import raises
from natsort import (
    natsorted,
    natsort_key,
    natsort_keygen,
    ns,
)
# from natsort.utils import _natsort_key


def test_natsort_key_public_raises_DeprecationWarning_when_called():
    # Identical to _natsort_key
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
