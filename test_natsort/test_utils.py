# -*- coding: utf-8 -*-
"""These test the utils.py functions."""

import locale
from operator import itemgetter
from pytest import raises
from natsort.ns_enum import ns
from natsort.utils import _input_parser, _py3_safe, _natsort_key, _args_to_enum
from natsort.utils import _float_sign_exp_re, _float_nosign_exp_re, _float_sign_noexp_re
from natsort.utils import _float_nosign_noexp_re, _int_nosign_re, _int_sign_re
from natsort.locale_help import use_pyicu

try:
    from fastnumbers import fast_float, fast_int
except ImportError:
    from natsort.fake_fastnumbers import fast_float, fast_int

try:
    import pathlib
except ImportError:
    has_pathlib = False
else:
    has_pathlib = True


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
    # Converts pathlib PurePath (and subclass) objects to string before sorting
    if has_pathlib:
        assert _natsort_key(pathlib.Path('../Folder (10)/file (2).tar.gz'), key=None, alg=ns.PATH) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))

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
