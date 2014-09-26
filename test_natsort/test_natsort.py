# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import unicode_literals
import warnings
import locale
from operator import itemgetter
from pytest import raises
from natsort import natsorted, index_natsorted, natsort_key, versorted, index_versorted
from natsort import humansorted, index_humansorted, natsort_keygen, order_by_index, ns
from natsort.utils import _natsort_key


def test_natsort_key_public():

    # Identical to _natsort_key
    # But it raises a depreciation warning
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert natsort_key('a-5.034e2') == _natsort_key('a-5.034e2', key=None, alg=ns.F)
        assert len(w) == 1
        assert "natsort_key is depreciated as of 3.4.0, please use natsort_keygen" in str(w[-1].message)
        assert natsort_key('a-5.034e2', number_type=float, signed=False, exp=False) == _natsort_key('a-5.034e2', key=None, alg=ns.F | ns.U | ns.N)
        assert natsort_key('a-5.034e2', alg=ns.F | ns.U | ns.N) == _natsort_key('a-5.034e2', key=None, alg=ns.F | ns.U | ns.N)

    # It is called for each element in a list when sorting
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
        a.sort(key=natsort_key)
        assert len(w) == 7


def test_natsort_keygen():

    # Creates equivalent natsort keys
    a = 'a-5.034e1'
    assert natsort_keygen()(a) == _natsort_key(a, key=None, alg=ns.F)
    assert natsort_keygen(alg=ns.UNSIGNED)(a) == _natsort_key(a, key=None, alg=ns.U)
    assert natsort_keygen(alg=ns.NOEXP)(a) == _natsort_key(a, key=None, alg=ns.N)
    assert natsort_keygen(alg=ns.U | ns.N)(a) == _natsort_key(a, key=None, alg=ns.U | ns.N)
    assert natsort_keygen(alg=ns.INT)(a) == _natsort_key(a, key=None, alg=ns.INT)
    assert natsort_keygen(alg=ns.I | ns.U)(a) == _natsort_key(a, key=None, alg=ns.I | ns.U)
    assert natsort_keygen(alg=ns.VERSION)(a) == _natsort_key(a, key=None, alg=ns.V)
    assert natsort_keygen(alg=ns.PATH)(a) == _natsort_key(a, key=None, alg=ns.PATH)

    # Custom keys are more straightforward with keygen
    f1 = natsort_keygen(key=lambda x: x.upper())
    f2 = lambda x: _natsort_key(x, key=lambda y: y.upper(), alg=ns.F)
    assert f1(a) == f2(a)

    # It also makes sorting lists in-place easier (no lambdas!)
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    b = a[:]
    a.sort(key=natsort_keygen(alg=ns.I))
    assert a == natsorted(b, alg=ns.I)


def test_natsorted():

    # Basic usage
    a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
    assert natsorted(a) == ['a1', 'a2', 'a4', 'a5', 'a6', 'a9', 'a10']

    # Number types
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a)                          == ['a50', 'a50.300', 'a50.31', 'a5.034e1', 'a50.4', 'a51.']
    assert natsorted(a, alg=ns.NOEXP | ns.FLOAT) == ['a5.034e1', 'a50', 'a50.300', 'a50.31', 'a50.4', 'a51.']
    assert natsorted(a, alg=ns.INT)              == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.']
    assert natsorted(a, alg=ns.DIGIT)            == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.']

    # Signed option
    a = ['a-5', 'a7', 'a+2']
    assert natsorted(a)                  == ['a-5', 'a+2', 'a7']
    assert natsorted(a, alg=ns.UNSIGNED) == ['a7', 'a+2', 'a-5']

    # Number type == None
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert natsorted(a)               == ['1.10.1', '1.11', '1.11.4', '1.9.9a', '1.9.9b']
    assert natsorted(a, alg=ns.DIGIT) == ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']

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
    assert natsorted(a, alg=ns.PATH) == ['/p/Folder/file.tar.gz',
                                         '/p/Folder (1)/file.tar.gz',
                                         '/p/Folder (1)/file (1).tar.gz',
                                         '/p/Folder (10)/file.tar.gz']

    # You can sort paths and numbers, not that you'd want to
    a = ['/Folder (9)/file.exe', 43]
    assert natsorted(a, alg=ns.PATH) == [43, '/Folder (9)/file.exe']

    # You can modify how case is interpreted in your sorting.
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a) == ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']
    assert natsorted(a, alg=ns.IGNORECASE) == ['Apple', 'apple', 'Banana', 'banana', 'corn', 'Corn']
    assert natsorted(a, alg=ns.LOWERCASEFIRST) == ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']
    assert natsorted(a, alg=ns.GROUPLETTERS) == ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']
    assert natsorted(a, alg=ns.G | ns.LF) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']

    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b) == [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b, alg=ns.LOWERCASEFIRST) == [('a3', 'a1'), ('A5', 'a6')]
    assert natsorted(b, alg=ns.IGNORECASE) == [('a3', 'a1'), ('A5', 'a6')]

    # You can also do locale-aware sorting
    locale.setlocale(locale.LC_ALL, str('en_US.UTF-8'))
    assert natsorted(a, alg=ns.LOCALE) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']
    a = ['c', 'ä', 'b', 'a5,6', 'a5,50']
    assert natsorted(a, alg=ns.LOCALE) == ['a5,6', 'a5,50', 'ä', 'b', 'c']

    locale.setlocale(locale.LC_ALL, str('de_DE.UTF-8'))
    assert natsorted(a, alg=ns.LOCALE) == ['a5,50', 'a5,6', 'ä', 'b', 'c']
    locale.setlocale(locale.LC_ALL, str(''))


def test_versorted():

    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert versorted(a) == natsorted(a, alg=ns.VERSION)
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
    assert versorted(a, alg=ns.PATH) == ['/p/Folder/file1.1.0.tar.gz',
                                         '/p/Folder (1)/file1.1.0.tar.gz',
                                         '/p/Folder (1)/file1.1.0 (1).tar.gz',
                                         '/p/Folder (10)/file1.1.0.tar.gz']


def test_humansorted():

    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert humansorted(a) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']
    assert humansorted(a) == natsorted(a, alg=ns.LOCALE)
    assert humansorted(a, reverse=True) == humansorted(a)[::-1]


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
    assert index_natsorted(a, alg=ns.PATH) == [1, 2, 0]


def test_index_versorted():

    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert index_versorted(a) == index_natsorted(a, alg=ns.VERSION)
    assert index_versorted(a, reverse=True) == index_versorted(a)[::-1]
    a = [('a', '1.9.9a'), ('a', '1.11'), ('a', '1.9.9b'),
         ('a', '1.11.4'), ('a', '1.10.1')]
    assert index_versorted(a) == [0, 2, 4, 1, 3]

    # It can sort paths too
    a = ['/p/Folder (10)/file1.1.0.tar.gz',
         '/p/Folder/file1.1.0.tar.gz',
         '/p/Folder (1)/file1.1.0 (1).tar.gz',
         '/p/Folder (1)/file1.1.0.tar.gz']
    assert index_versorted(a, alg=ns.PATH) == [1, 3, 2, 0]


def test_index_humansorted():

    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert index_humansorted(a) == [4, 0, 5, 3, 1, 2]
    assert index_humansorted(a) == index_natsorted(a, alg=ns.LOCALE)
    assert index_humansorted(a, reverse=True) == index_humansorted(a)[::-1]


def test_order_by_index():

    # Return the indexes of how the iterable would be sorted.
    a = ['num3', 'num5', 'num2']
    index = [2, 0, 1]
    assert order_by_index(a, index) == ['num2', 'num3', 'num5']
    assert order_by_index(a, index) == [a[i] for i in index]
    assert order_by_index(a, index, True) != [a[i] for i in index]
    assert list(order_by_index(a, index, True)) == [a[i] for i in index]
