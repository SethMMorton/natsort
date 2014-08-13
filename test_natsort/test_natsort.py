# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
import warnings
from operator import itemgetter
from pytest import raises
from natsort import natsorted, index_natsorted, natsort_key, versorted, index_versorted, natsort_keygen, order_by_index
from natsort.natsort import _number_finder, _py3_safe, _natsort_key
from natsort.natsort import float_sign_exp_re, float_nosign_exp_re, float_sign_noexp_re
from natsort.natsort import float_nosign_noexp_re, int_nosign_re, int_sign_re

try:
    from fastnumbers import fast_float, fast_int
except ImportError:
    from natsort.fake_fastnumbers import fast_float, fast_int


def test_number_finder():

    assert _number_finder('a5+5.034e-1', float_sign_exp_re,     fast_float, False) == ['a', 5.0, 0.5034]
    assert _number_finder('a5+5.034e-1', float_nosign_exp_re,   fast_float, False) == ['a', 5.0, '+', 0.5034]
    assert _number_finder('a5+5.034e-1', float_sign_noexp_re,   fast_float, False) == ['a', 5.0, 5.034, 'e', -1.0]
    assert _number_finder('a5+5.034e-1', float_nosign_noexp_re, fast_float, False) == ['a', 5.0, '+', 5.034, 'e-', 1.0]
    assert _number_finder('a5+5.034e-1', int_nosign_re,         fast_int,   False) == ['a', 5, '+', 5, '.', 34, 'e-', 1]
    assert _number_finder('a5+5.034e-1', int_sign_re,           fast_int,   False) == ['a', 5, 5, '.', 34, 'e', -1]

    assert _number_finder('a5+5.034e-1', float_sign_exp_re,     fast_float, True) == ['a', 5.0, '', 0.5034]
    assert _number_finder('a5+5.034e-1', float_nosign_exp_re,   fast_float, True) == ['a', 5.0, '+', 0.5034]
    assert _number_finder('a5+5.034e-1', float_sign_noexp_re,   fast_float, True) == ['a', 5.0, '', 5.034, 'e', -1.0]
    assert _number_finder('a5+5.034e-1', float_nosign_noexp_re, fast_float, True) == ['a', 5.0, '+', 5.034, 'e-', 1.0]
    assert _number_finder('a5+5.034e-1', int_nosign_re,         fast_int,   True) == ['a', 5, '+', 5, '.', 34, 'e-', 1]
    assert _number_finder('a5+5.034e-1', int_sign_re,           fast_int,   True) == ['a', 5, '', 5, '.', 34, 'e', -1]

    assert _number_finder('6a5+5.034e-1', float_sign_exp_re,    fast_float, False) == ['', 6.0, 'a', 5.0, 0.5034]
    assert _number_finder('6a5+5.034e-1', float_sign_exp_re,    fast_float, True)  == ['', 6.0, 'a', 5.0, '', 0.5034]


def test_py3_safe():

    assert _py3_safe(['a', 'b', 'c']) == ['a', 'b', 'c']
    assert _py3_safe(['a']) == ['a']
    assert _py3_safe(['a', 5]) == ['a', 5]
    assert _py3_safe([5, 9]) == [5, '', 9]


def test_natsort_key_private():

    a = ['num3', 'num5', 'num2']
    a.sort(key=_natsort_key)
    assert a == ['num2', 'num3', 'num5']

    # The below illustrates how the key works, and how the different options affect sorting.
    assert _natsort_key('a-5.034e2')                                             == ('a', -503.4)
    assert _natsort_key('a-5.034e2', number_type=float, signed=True,  exp=True)  == ('a', -503.4)
    assert _natsort_key('a-5.034e2', number_type=float, signed=True,  exp=False) == ('a', -5.034, 'e', 2.0)
    assert _natsort_key('a-5.034e2', number_type=float, signed=False, exp=True)  == ('a-', 503.4)
    assert _natsort_key('a-5.034e2', number_type=float, signed=False, exp=False) == ('a-', 5.034, 'e', 2.0)
    assert _natsort_key('a-5.034e2', number_type=int)                            == ('a', -5, '.', 34, 'e', 2)
    assert _natsort_key('a-5.034e2', number_type=int, signed=False)              == ('a-', 5, '.', 34, 'e', 2)
    assert _natsort_key('a-5.034e2', number_type=None) == _natsort_key('a-5.034e2', number_type=int, signed=False)
    assert _natsort_key('a-5.034e2', key=lambda x: x.upper()) == ('A', -503.4)

    # Iterables are parsed recursively so you can sort lists of lists.
    assert _natsort_key(('a1', 'a-5.034e2')) == (('a', 1.0), ('a', -503.4))
    assert _natsort_key(('a1', 'a-5.034e2'), number_type=None) == (('a', 1), ('a-', 5, '.', 34, 'e', 2))
    # A key is applied before recursion, but not in the recursive calls.
    assert _natsort_key(('a1', 'a-5.034e2'), key=itemgetter(1)) == ('a', -503.4)

    # Strings that lead with a number get an empty string at the front of the tuple.
    # This is designed to get around the "unorderable types" issue.
    assert _natsort_key(('15a', '6')) == (('', 15.0, 'a'), ('', 6.0))
    assert _natsort_key(10) == ('', 10)

    # Turn on as_path to split a file path into components
    assert _natsort_key('/p/Folder (10)/file34.5nm (2).tar.gz', as_path=True) == (('/',), ('p', ), ('Folder (', 10.0, ')',), ('file', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))
    assert _natsort_key('../Folder (10)/file (2).tar.gz', as_path=True) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))
    assert _natsort_key('Folder (10)/file.f34.5nm (2).tar.gz', as_path=True) == (('Folder (', 10.0, ')',), ('file.f', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))

    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    assert _natsort_key(10, as_path=True) == (('', 10),)
    # as_path also handles recursion well.
    assert _natsort_key(('/Folder', '/Folder (1)'), as_path=True) == ((('/',), ('Folder',)), (('/',), ('Folder (', 1.0, ')')))

    # Turn on py3_safe to put a '' between adjacent numbers
    assert _natsort_key('43h7+3', py3_safe=True) == ('', 43.0, 'h', 7.0, '', 3.0)

    # Invalid arguments give the correct response
    with raises(ValueError) as err:
        _natsort_key('a', number_type='float')
    assert str(err.value) == "_natsort_key: 'number_type' parameter 'float' invalid"
    with raises(ValueError) as err:
        _natsort_key('a', signed='True')
    assert str(err.value) == "_natsort_key: 'signed' parameter 'True' invalid"
    with raises(ValueError) as err:
        _natsort_key('a', exp='False')
    assert str(err.value) == "_natsort_key: 'exp' parameter 'False' invalid"


def test_natsort_key_public():

    # Identical to _natsort_key
    # But it raises a depreciation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert natsort_key('a-5.034e2') == _natsort_key('a-5.034e2')
        assert len(w) == 1
        assert "natsort_key is depreciated as of 3.4.0, please use natsort_keygen" in str(w[-1].message)
        assert natsort_key('a-5.034e2', number_type=float, signed=False, exp=False) == _natsort_key('a-5.034e2', number_type=float, signed=False, exp=False)

    # It is called for each element in a list when sorting
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
        a.sort(key=natsort_key)
        assert len(w) == 7


def test_natsort_keygen():

    # Creates equivalent natsort keys
    a = 'a-5.034e1'
    assert natsort_keygen()(a) == _natsort_key(a)
    assert natsort_keygen(signed=False)(a) == _natsort_key(a, signed=False)
    assert natsort_keygen(exp=False)(a) == _natsort_key(a, exp=False)
    assert natsort_keygen(signed=False, exp=False)(a) == _natsort_key(a, signed=False, exp=False)
    assert natsort_keygen(number_type=int)(a) == _natsort_key(a, number_type=int)
    assert natsort_keygen(number_type=int, signed=False)(a) == _natsort_key(a, number_type=int, signed=False)
    assert natsort_keygen(number_type=None)(a) == _natsort_key(a, number_type=None)
    assert natsort_keygen(as_path=True)(a) == _natsort_key(a, as_path=True)

    # Custom keys are more straightforward with keygen
    f1 = natsort_keygen(key=lambda x: x.upper())
    f2 = lambda x: _natsort_key(x, key=lambda y: y.upper())
    assert f1(a) == f2(a)

    # It also makes sorting lists in-place easier (no lambdas!)
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    b = a[:]
    a.sort(key=natsort_keygen(number_type=int))
    assert a == natsorted(b, number_type=int)


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

    # natsort will recursively descend into lists of lists so you can
    # sort by the sublist contents.
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert natsorted(data) == [['a1', 'a5'], ['a1', 'a40'],
                               ['a2', 'a5'], ['a10', 'a1']]

    # You can pass a key to do non-standard sorting rules
    b = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    c = [('c', 'num2'), ('a', 'num3'), ('b', 'num5')]
    assert natsorted(b, key=itemgetter(1)) == c

    # Reversing the order is allowed
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    b = ['a50', 'a50.300', 'a50.31', 'a5.034e1', 'a50.4', 'a51.']
    assert natsorted(a, reverse=True) == b[::-1]

    # Sorting paths just got easier
    a = ['/p/Folder (10)/file.tar.gz',
         '/p/Folder/file.tar.gz',
         '/p/Folder (1)/file (1).tar.gz',
         '/p/Folder (1)/file.tar.gz']
    assert natsorted(a) == ['/p/Folder (1)/file (1).tar.gz',
                            '/p/Folder (1)/file.tar.gz',
                            '/p/Folder (10)/file.tar.gz',
                            '/p/Folder/file.tar.gz']
    assert natsorted(a, as_path=True) == ['/p/Folder/file.tar.gz',
                                          '/p/Folder (1)/file.tar.gz',
                                          '/p/Folder (1)/file (1).tar.gz',
                                          '/p/Folder (10)/file.tar.gz']

    # You can sort paths and numbers, not that you'd want to
    a = ['/Folder (9)/file.exe', 43]
    assert natsorted(a, as_path=True) == [43, '/Folder (9)/file.exe']


def test_versorted():

    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert versorted(a) == natsorted(a, number_type=None)
    assert versorted(a, reverse=True) == versorted(a)[::-1]
    a = [('a', '1.9.9a'), ('a', '1.11'), ('a', '1.9.9b'),
         ('a', '1.11.4'), ('a', '1.10.1')]
    assert versorted(a) == [('a', '1.9.9a'), ('a', '1.9.9b'), ('a', '1.10.1'),
                            ('a', '1.11'), ('a', '1.11.4')]

    # Sorting paths just got easier
    a = ['/p/Folder (10)/file1.1.0.tar.gz',
         '/p/Folder/file1.1.0.tar.gz',
         '/p/Folder (1)/file1.1.0 (1).tar.gz',
         '/p/Folder (1)/file1.1.0.tar.gz']
    assert versorted(a) == ['/p/Folder (1)/file1.1.0 (1).tar.gz',
                            '/p/Folder (1)/file1.1.0.tar.gz',
                            '/p/Folder (10)/file1.1.0.tar.gz',
                            '/p/Folder/file1.1.0.tar.gz']
    assert versorted(a, as_path=True) == ['/p/Folder/file1.1.0.tar.gz',
                                          '/p/Folder (1)/file1.1.0.tar.gz',
                                          '/p/Folder (1)/file1.1.0 (1).tar.gz',
                                          '/p/Folder (10)/file1.1.0.tar.gz']


def test_index_natsorted():

    # Return the indexes of how the iterable would be sorted.
    a = ['num3', 'num5', 'num2']
    b = ['foo', 'bar', 'baz']
    index = index_natsorted(a)
    assert index == [2, 0, 1]
    assert [a[i] for i in index] == ['num2', 'num3', 'num5']
    assert [b[i] for i in index] == ['baz', 'foo', 'bar']
    assert index_natsorted(a, reverse=True) == [1, 0, 2]

    # It accepts a key argument.
    c = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert index_natsorted(c, key=itemgetter(1)) == [2, 0, 1]

    # It can avoid "unorderable types" on Python 3
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert index_natsorted(a) == [3, 1, 0, 2]

    # It can sort lists of lists.
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert index_natsorted(data) == [0, 1, 3, 2]

    # It can sort paths too
    a = ['/p/Folder (10)/',
         '/p/Folder/',
         '/p/Folder (1)/']
    assert index_natsorted(a, as_path=True) == [1, 2, 0]


def test_index_versorted():

    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert index_versorted(a) == index_natsorted(a, number_type=None)
    assert index_versorted(a, reverse=True) == index_versorted(a)[::-1]
    a = [('a', '1.9.9a'), ('a', '1.11'), ('a', '1.9.9b'),
         ('a', '1.11.4'), ('a', '1.10.1')]
    assert index_versorted(a) == [0, 2, 4, 1, 3]

    # It can sort paths too
    a = ['/p/Folder (10)/file1.1.0.tar.gz',
         '/p/Folder/file1.1.0.tar.gz',
         '/p/Folder (1)/file1.1.0 (1).tar.gz',
         '/p/Folder (1)/file1.1.0.tar.gz']
    assert index_versorted(a, as_path=True) == [1, 3, 2, 0]


def test_order_by_index():

    # Return the indexes of how the iterable would be sorted.
    a = ['num3', 'num5', 'num2']
    index = [2, 0, 1]
    assert order_by_index(a, index) == ['num2', 'num3', 'num5']
    assert order_by_index(a, index) == [a[i] for i in index]
    assert order_by_index(a, index, True) != [a[i] for i in index]
    assert list(order_by_index(a, index, True)) == [a[i] for i in index]
