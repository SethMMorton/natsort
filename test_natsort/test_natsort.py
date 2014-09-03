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
from natsort import humansorted, index_humansorted, natsort_keygen, order_by_index
from natsort.natsort import _input_parser, _py3_safe, _natsort_key, _args_to_enum
from natsort.natsort import _float_sign_exp_re, _float_nosign_exp_re, _float_sign_noexp_re
from natsort.natsort import _float_nosign_noexp_re, _int_nosign_re, _int_sign_re
from natsort.natsort import ns
from natsort.locale_help import use_pyicu

try:
    from fastnumbers import fast_float, fast_int
except ImportError:
    from natsort.fake_fastnumbers import fast_float, fast_int


def test_args_to_enum():

    assert _args_to_enum(float, True, True, False, False) == ns.F
    assert _args_to_enum(float, True, False, False, False) == ns.F | ns.N
    assert _args_to_enum(float, False, True, False, False) == ns.F | ns.U
    assert _args_to_enum(float, False, False, False, False) == ns.F | ns.U | ns.N
    assert _args_to_enum(float, True, True, True, True) == ns.F | ns.P | ns.T
    assert _args_to_enum(int, True, True, True, False) == ns.I | ns.P
    assert _args_to_enum(int, False, True, False, True) == ns.I | ns.U | ns.T
    assert _args_to_enum(None, True, True, False, False) == ns.I | ns.U


def test_input_parser():

    # fttt = (fast_float, True, True, True)
    # fttf = (fast_float, True, True, False)
    ftft = (fast_float, True, False, True)
    ftff = (fast_float, True, False, False)
    # fftt = (fast_float, False, True, True)
    # ffft = (fast_float, False, False, True)
    # fftf = (fast_float, False, True, False)
    ffff = (fast_float, False, False, False)
    ittt = (fast_int, True, True, True)
    ittf = (fast_int, True, True, False)
    itft = (fast_int, True, False, True)
    itff = (fast_int, True, False, False)
    # iftt = (fast_int, False, True, True)
    # ifft = (fast_int, False, False, True)
    # iftf = (fast_int, False, True, False)
    ifff = (fast_int, False, False, False)

    assert _input_parser('a5+5.034e-1', _float_sign_exp_re,     *ffff) == ['a', 5.0, 0.5034]
    assert _input_parser('a5+5.034e-1', _float_nosign_exp_re,   *ffff) == ['a', 5.0, '+', 0.5034]
    assert _input_parser('a5+5.034e-1', _float_sign_noexp_re,   *ffff) == ['a', 5.0, 5.034, 'e', -1.0]
    assert _input_parser('a5+5.034e-1', _float_nosign_noexp_re, *ffff) == ['a', 5.0, '+', 5.034, 'e-', 1.0]
    assert _input_parser('a5+5.034e-1', _int_nosign_re,         *ifff) == ['a', 5, '+', 5, '.', 34, 'e-', 1]
    assert _input_parser('a5+5.034e-1', _int_sign_re,           *ifff) == ['a', 5, 5, '.', 34, 'e', -1]

    assert _input_parser('a5+5.034e-1', _float_sign_exp_re,     *ftff) == ['a', 5.0, '', 0.5034]
    assert _input_parser('a5+5.034e-1', _float_nosign_exp_re,   *ftff) == ['a', 5.0, '+', 0.5034]
    assert _input_parser('a5+5.034e-1', _float_sign_noexp_re,   *ftff) == ['a', 5.0, '', 5.034, 'e', -1.0]
    assert _input_parser('a5+5.034e-1', _float_nosign_noexp_re, *ftff) == ['a', 5.0, '+', 5.034, 'e-', 1.0]
    assert _input_parser('a5+5.034e-1', _int_nosign_re,         *itff) == ['a', 5, '+', 5, '.', 34, 'e-', 1]
    assert _input_parser('a5+5.034e-1', _int_sign_re,           *itff) == ['a', 5, '', 5, '.', 34, 'e', -1]

    assert _input_parser('6a5+5.034e-1', _float_sign_exp_re,    *ffff) == ['', 6.0, 'a', 5.0, 0.5034]
    assert _input_parser('6a5+5.034e-1', _float_sign_exp_re,    *ftff) == ['', 6.0, 'a', 5.0, '', 0.5034]

    assert _input_parser('A5+5.034E-1', _float_sign_exp_re,     *ftft) == ['aA', 5.0, '', 0.5034]
    assert _input_parser('A5+5.034E-1', _int_nosign_re,         *itft) == ['aA', 5, '++', 5, '..', 34, 'eE--', 1]

    locale.setlocale(locale.LC_NUMERIC, str('en_US.UTF-8'))
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert _input_parser('A5+5.034E-1', _int_nosign_re,         *ittf) == [strxfrm('A'), 5, strxfrm('+'), 5, strxfrm('.'), 34, strxfrm('E-'), 1]
    assert _input_parser('A5+5.034E-1', _int_nosign_re,         *ittt) == [strxfrm('aA'), 5, strxfrm('++'), 5, strxfrm('..'), 34, strxfrm('eE--'), 1]
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_py3_safe():

    assert _py3_safe(['a', 'b', 'c']) == ['a', 'b', 'c']
    assert _py3_safe(['a']) == ['a']
    assert _py3_safe(['a', 5]) == ['a', 5]
    assert _py3_safe([5, 9]) == [5, '', 9]


def test_natsort_key_private():

    # The below illustrates how the key works, and how the different options affect sorting.
    assert _natsort_key('a-5.034e2', key=None, alg=ns.F)                         == ('a', -503.4)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.FLOAT)                     == ('a', -503.4)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.FLOAT | ns.NOEXP)          == ('a', -5.034, 'e', 2.0)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.NOEXP)                     == ('a', -5.034, 'e', 2.0)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.UNSIGNED)                  == ('a-', 503.4)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.UNSIGNED | ns.NOEXP)       == ('a-', 5.034, 'e', 2.0)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.INT)                       == ('a', -5, '.', 34, 'e', 2)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.INT | ns.NOEXP)            == ('a', -5, '.', 34, 'e', 2)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.INT | ns.UNSIGNED)         == ('a-', 5, '.', 34, 'e', 2)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.VERSION) == _natsort_key('a-5.034e2', key=None, alg=ns.INT | ns.UNSIGNED)
    assert _natsort_key('a-5.034e2', key=None, alg=ns.DIGIT) == _natsort_key('a-5.034e2', key=None, alg=ns.VERSION)
    assert _natsort_key('a-5.034e2', key=lambda x: x.upper(), alg=ns.F) == ('A', -503.4)

    # Iterables are parsed recursively so you can sort lists of lists.
    assert _natsort_key(('a1', 'a-5.034e2'), key=None, alg=ns.F) == (('a', 1.0), ('a', -503.4))
    assert _natsort_key(('a1', 'a-5.034e2'), key=None, alg=ns.V) == (('a', 1), ('a-', 5, '.', 34, 'e', 2))
    # A key is applied before recursion, but not in the recursive calls.
    assert _natsort_key(('a1', 'a-5.034e2'), key=itemgetter(1), alg=ns.F) == ('a', -503.4)

    # Strings that lead with a number get an empty string at the front of the tuple.
    # This is designed to get around the "unorderable types" issue.
    assert _natsort_key(('15a', '6'), key=None, alg=ns.F) == (('', 15.0, 'a'), ('', 6.0))
    assert _natsort_key(10, key=None, alg=ns.F) == ('', 10)

    # Turn on as_path to split a file path into components
    assert _natsort_key('/p/Folder (10)/file34.5nm (2).tar.gz', key=None, alg=ns.PATH) == (('/',), ('p', ), ('Folder (', 10.0, ')',), ('file', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))
    assert _natsort_key('../Folder (10)/file (2).tar.gz', key=None, alg=ns.PATH) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))
    assert _natsort_key('Folder (10)/file.f34.5nm (2).tar.gz', key=None, alg=ns.PATH) == (('Folder (', 10.0, ')',), ('file.f', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))

    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    assert _natsort_key(10, key=None, alg=ns.PATH) == (('', 10),)
    # as_path also handles recursion well.
    assert _natsort_key(('/Folder', '/Folder (1)'), key=None, alg=ns.PATH) == ((('/',), ('Folder',)), (('/',), ('Folder (', 1.0, ')')))

    # Turn on py3_safe to put a '' between adjacent numbers
    assert _natsort_key('43h7+3', key=None, alg=ns.TYPESAFE) == ('', 43.0, 'h', 7.0, '', 3.0)

    # Invalid arguments give the correct response
    with raises(ValueError) as err:
        _natsort_key('a', key=None, alg='1')
    assert str(err.value) == "_natsort_key: 'alg' argument must be from the enum 'ns', got 1"

    # Changing the sort order of strings
    assert _natsort_key('Apple56', key=None, alg=ns.F) == ('Apple', 56.0)
    assert _natsort_key('Apple56', key=None, alg=ns.IGNORECASE) == ('apple', 56.0)
    assert _natsort_key('Apple56', key=None, alg=ns.LOWERCASEFIRST) == ('aPPLE', 56.0)
    assert _natsort_key('Apple56', key=None, alg=ns.GROUPLETTERS) == ('aAppppllee', 56.0)
    assert _natsort_key('Apple56', key=None, alg=ns.G | ns.LF) == ('aapPpPlLeE', 56.0)

    # Locale aware sorting
    locale.setlocale(locale.LC_NUMERIC, str('en_US.UTF-8'))
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert _natsort_key('Apple56.5', key=None, alg=ns.LOCALE) == (strxfrm('Apple'), 56.5)
    assert _natsort_key('Apple56,5', key=None, alg=ns.LOCALE) == (strxfrm('Apple'), 56.0, strxfrm(','), 5.0)

    locale.setlocale(locale.LC_NUMERIC, str('de_DE.UTF-8'))
    if use_pyicu:
        strxfrm = get_pyicu_transform(getlocale())
    assert _natsort_key('Apple56.5', key=None, alg=ns.LOCALE) == (strxfrm('Apple'), 56.5)
    assert _natsort_key('Apple56,5', key=None, alg=ns.LOCALE) == (strxfrm('Apple'), 56.5)
    locale.setlocale(locale.LC_NUMERIC, str(''))


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
