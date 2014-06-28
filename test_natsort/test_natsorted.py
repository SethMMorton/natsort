# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from operator import itemgetter
from pytest import raises
from natsort import natsorted, index_natsorted, natsort_key, versorted, index_versorted
from natsort.natsort import _remove_empty, _number_finder, _py3_safe
from natsort.natsort import float_sign_exp_re, float_nosign_exp_re, float_sign_noexp_re
from natsort.natsort import float_nosign_noexp_re, int_nosign_re, int_sign_re


def test__remove_empty():

    assert _remove_empty(['a', 2, '', 'b', '']) == ['a', 2, 'b']
    assert _remove_empty(['a', 2, 'b', ''])     == ['a', 2, 'b']
    assert _remove_empty(['a', 2, 'b'])         == ['a', 2, 'b']


def test_number_finder():

    assert _number_finder('a5+5.034e-1', float_sign_exp_re,     float, False) == ['a', 5.0, 0.5034]
    assert _number_finder('a5+5.034e-1', float_nosign_exp_re,   float, False) == ['a', 5.0, '+', 0.5034]
    assert _number_finder('a5+5.034e-1', float_sign_noexp_re,   float, False) == ['a', 5.0, 5.034, 'e', -1.0]
    assert _number_finder('a5+5.034e-1', float_nosign_noexp_re, float, False) == ['a', 5.0, '+', 5.034, 'e-', 1.0]
    assert _number_finder('a5+5.034e-1', int_nosign_re,         int,   False) == ['a', 5, '+', 5, '.', 34, 'e-', 1]
    assert _number_finder('a5+5.034e-1', int_sign_re,           int,   False) == ['a', 5, 5, '.', 34, 'e', -1]

    assert _number_finder('a5+5.034e-1', float_sign_exp_re,     float, True) == ['a', 5.0, '', 0.5034]
    assert _number_finder('a5+5.034e-1', float_nosign_exp_re,   float, True) == ['a', 5.0, '+', 0.5034]
    assert _number_finder('a5+5.034e-1', float_sign_noexp_re,   float, True) == ['a', 5.0, '', 5.034, 'e', -1.0]
    assert _number_finder('a5+5.034e-1', float_nosign_noexp_re, float, True) == ['a', 5.0, '+', 5.034, 'e-', 1.0]
    assert _number_finder('a5+5.034e-1', int_nosign_re,         int,   True) == ['a', 5, '+', 5, '.', 34, 'e-', 1]
    assert _number_finder('a5+5.034e-1', int_sign_re,           int,   True) == ['a', 5, '', 5, '.', 34, 'e', -1]

    assert _number_finder('6a5+5.034e-1', float_sign_exp_re,    float, False) == ['', 6.0, 'a', 5.0, 0.5034]
    assert _number_finder('6a5+5.034e-1', float_sign_exp_re,    float, True)  == ['', 6.0, 'a', 5.0, '', 0.5034]


def test_py3_safe():

    assert _py3_safe(['a', 'b', 'c']) == ['a', 'b', 'c']
    assert _py3_safe(['a']) == ['a']
    assert _py3_safe(['a', 5]) == ['a', 5]
    assert _py3_safe([5, 9]) == [5, '', 9]


def test_natsort_key():

    a = ['num3', 'num5', 'num2']
    a.sort(key=natsort_key)
    assert a == ['num2', 'num3', 'num5']

    # The below illustrates how the key works, and how the different options affect sorting.
    assert natsort_key('a-5.034e1')                                             == ('a', -50.34)
    assert natsort_key('a-5.034e1', number_type=float, signed=True,  exp=True)  == ('a', -50.34)
    assert natsort_key('a-5.034e1', number_type=float, signed=True,  exp=False) == ('a', -5.034, 'e', 1.0)
    assert natsort_key('a-5.034e1', number_type=float, signed=False, exp=True)  == ('a-', 50.34)
    assert natsort_key('a-5.034e1', number_type=float, signed=False, exp=False) == ('a-', 5.034, 'e', 1.0)
    assert natsort_key('a-5.034e1', number_type=int)                            == ('a', -5, '.', 34, 'e', 1)
    assert natsort_key('a-5.034e1', number_type=int, signed=False)              == ('a-', 5, '.', 34, 'e', 1)
    assert natsort_key('a-5.034e1', number_type=None) == natsort_key('a-5.034e1', number_type=int, signed=False)

    # Iterables are parsed recursively so you can sort lists of lists.
    assert natsort_key(('a1', 'a10')) == (('a', 1.0), ('a', 10.0))

    # Strings that lead with a number get an empty string at the front of the tuple.
    # This is designed to get around the "unorderable types" issue.
    assert natsort_key(('15a', '6')) == (('', 15.0, 'a'), ('', 6.0))
    assert natsort_key(10) == ('', 10)

    # Turn on py3_safe to put a '' between adjacent numbers
    assert natsort_key('43h7+3', py3_safe=True) == ('', 43.0, 'h', 7.0, '', 3.0)

    # Invalid arguments give the correct response
    with raises(ValueError) as err:
        natsort_key('a', number_type='float')
    assert str(err.value) == "natsort_key: 'number_type' parameter 'float' invalid"
    with raises(ValueError) as err:
        natsort_key('a', signed='True')
    assert str(err.value) == "natsort_key: 'signed' parameter 'True' invalid"
    with raises(ValueError) as err:
        natsort_key('a', exp='False')
    assert str(err.value) == "natsort_key: 'exp' parameter 'False' invalid"


def test_natsorted():

    # Basic usage
    a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
    assert natsorted(a) == ['a1', 'a2', 'a4', 'a5', 'a6', 'a9', 'a10']

    # Number types
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a)                               == ['a50', 'a50.300', 'a50.31', 'a5.034e1', 'a50.4', 'a51.']
    assert natsorted(a, number_type=float, exp=False) == ['a5.034e1', 'a50', 'a50.300', 'a50.31', 'a50.4', 'a51.']
    assert natsorted(a, number_type=int)              == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.']
    assert natsorted(a, number_type=None)             == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.']

    # Signed option
    a = ['a-5', 'a7', 'a+2']
    assert natsorted(a)               == ['a-5', 'a+2', 'a7']
    assert natsorted(a, signed=False) == ['a7', 'a+2', 'a-5']

    # Number type == None
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert natsorted(a)                   == ['1.10.1', '1.11', '1.11.4', '1.9.9a', '1.9.9b']
    assert natsorted(a, number_type=None) == ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']

    # You can mix types with natsorted.  This can get around the new
    # 'unorderable types' issue with Python 3.
    a = [6, 4.5, '7', '2.5', 'a']
    assert natsorted(a) == ['2.5', 4.5, 6, '7', 'a']
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert natsorted(a) == ['5a5-4', '5a5b2', 46, 'af5']

    # You still can't sort non-iterables
    with raises(TypeError) as err:
        natsorted(100)
    assert str(err.value) == "'int' object is not iterable"

    # natsort will recursively descend into lists of lists so you can sort by the sublist contents.
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert natsorted(data) == [['a1', 'a5'], ['a1', 'a40'], ['a2', 'a5'], ['a10', 'a1']]

    # You can pass a key to do non-standard sorting rules
    b = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert natsorted(b, key=itemgetter(1)) == [('c', 'num2'), ('a', 'num3'), ('b', 'num5')]


def test_versorted():

    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert versorted(a) == natsorted(a, number_type=None)

def test_index_natsorted():
    
    # Return the indexes of how the iterable would be sorted.
    a = ['num3', 'num5', 'num2']
    b = ['foo', 'bar', 'baz']
    index = index_natsorted(a)
    assert index == [2, 0, 1]
    assert [a[i] for i in index] == ['num2', 'num3', 'num5']
    assert [b[i] for i in index] == ['baz', 'foo', 'bar']
    
    # It accepts a key argument.
    c = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert index_natsorted(c, key=itemgetter(1)) == [2, 0, 1]

    # It can avoid "unorderable types" on Python 3
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert index_natsorted(a) == [3, 1, 0, 2]


def test_index_versorted():

    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert index_versorted(a) == index_natsorted(a, number_type=None)
