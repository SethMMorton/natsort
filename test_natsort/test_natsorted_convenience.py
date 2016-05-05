# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import unicode_literals, print_function
from operator import itemgetter
from natsort.compat.py23 import PY_VERSION
from natsort import (
    natsorted,
    index_natsorted,
    versorted,
    index_versorted,
    humansorted,
    index_humansorted,
    realsorted,
    index_realsorted,
    order_by_index,
    ns,
    decoder,
    as_ascii,
    as_utf8,
)


def test_decoder_returns_function_that_can_decode_bytes_but_return_non_bytes_as_is():
    f = decoder('latin1')
    a = 'bytes'
    b = 14
    assert f(b'bytes') == a
    assert f(b) is b  # returns as-is, same object ID
    if PY_VERSION >= 3:
        assert f(a) is a  # same object returned on Python3 b/c only bytes has decode
    else:
        assert f(a) is not a
        assert f(a) == a  # not same object on Python2 because str can decode


def test_as_ascii_returns_bytes_as_ascii():
    assert decoder('ascii')(b'bytes') == as_ascii(b'bytes')


def test_as_utf8_returns_bytes_as_utf8():
    assert decoder('utf8')(b'bytes') == as_utf8(b'bytes')


def test_versorted_returns_results_identical_to_natsorted():
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    # versorted is retained for backwards compatibility
    assert versorted(a) == natsorted(a)


def test_realsorted_returns_results_identical_to_natsorted_with_REAL():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert realsorted(a) == natsorted(a, alg=ns.REAL)


def test_humansorted_returns_results_identical_to_natsorted_with_LOCALE():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert humansorted(a) == natsorted(a, alg=ns.LOCALE)


def test_index_natsorted_returns_integer_list_of_sort_order_for_input_list():
    a = ['num3', 'num5', 'num2']
    b = ['foo', 'bar', 'baz']
    index = index_natsorted(a)
    assert index == [2, 0, 1]
    assert [a[i] for i in index] == ['num2', 'num3', 'num5']
    assert [b[i] for i in index] == ['baz', 'foo', 'bar']


def test_index_natsorted_returns_reversed_integer_list_of_sort_order_for_input_list_with_reverse_option():
    a = ['num3', 'num5', 'num2']
    assert index_natsorted(a, reverse=True) == [1, 0, 2]


def test_index_natsorted_applies_key_function_before_sorting():
    c = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert index_natsorted(c, key=itemgetter(1)) == [2, 0, 1]


def test_index_natsorted_handles_unorderable_types_error_on_Python3():
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert index_natsorted(a) == [3, 1, 0, 2]


def test_index_natsorted_returns_integer_list_of_nested_input_list():
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert index_natsorted(data) == [0, 1, 3, 2]


def test_index_natsorted_returns_integer_list_in_proper_order_for_input_paths_with_PATH():
    a = ['/p/Folder (10)/',
         '/p/Folder/',
         '/p/Folder (1)/']
    assert index_natsorted(a, alg=ns.PATH) == [1, 2, 0]


def test_index_versorted_returns_results_identical_to_index_natsorted():
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    # index_versorted is retained for backwards compatibility
    assert index_versorted(a) == index_natsorted(a)


def test_index_realsorted_returns_results_identical_to_index_natsorted_with_REAL():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert index_realsorted(a) == index_natsorted(a, alg=ns.REAL)


def test_index_humansorted_returns_results_identical_to_index_natsorted_with_LOCALE():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert index_humansorted(a) == index_natsorted(a, alg=ns.LOCALE)


def test_order_by_index_sorts_list_according_to_order_of_integer_list():
    a = ['num3', 'num5', 'num2']
    index = [2, 0, 1]
    assert order_by_index(a, index) == ['num2', 'num3', 'num5']
    assert order_by_index(a, index) == [a[i] for i in index]


def test_order_by_index_returns_generator_with_iter_True():
    a = ['num3', 'num5', 'num2']
    index = [2, 0, 1]
    assert order_by_index(a, index, True) != [a[i] for i in index]
    assert list(order_by_index(a, index, True)) == [a[i] for i in index]
