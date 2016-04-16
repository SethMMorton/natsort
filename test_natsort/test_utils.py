# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import sys
import locale
import pathlib
import pytest
import string
from math import isnan, isinf
from operator import itemgetter, neg as op_neg
from itertools import chain
from pytest import raises
from natsort.ns_enum import ns
from natsort.utils import (
    _number_extracter,
    _sep_inserter,
    _natsort_key,
    _args_to_enum,
    _float_sign_exp_re,
    _float_nosign_exp_re,
    _float_sign_noexp_re,
    _float_nosign_noexp_re,
    _int_nosign_re,
    _int_sign_re,
    _do_decoding,
    _path_splitter,
    _fix_nan,
    chain_functions,
    _pre_split_function,
    _post_split_function,
    _ungroupletters,
)
from natsort.locale_help import locale_convert, groupletters
from natsort.compat.py23 import py23_str
from natsort.compat.locale import (
    use_pyicu,
    null_string,
    dumb_sort,
)
from natsort.compat.fastnumbers import (
    fast_float,
    fast_int,
)
from slow_splitters import (
    int_splitter,
    float_splitter,
    sep_inserter,
    add_leading_space_if_first_is_num,
)
from compat.locale import (
    load_locale,
    get_strxfrm,
    low,
    bad_uni_chars,
)
from compat.hypothesis import (
    assume,
    given,
    example,
    sampled_from,
    lists,
    text,
    floats,
    integers,
    use_hypothesis,
)

if sys.version[0] == '3':
    long = int

ichain = chain.from_iterable


def test_do_decoding_decodes_bytes_string_to_unicode():
    assert type(_do_decoding(b'bytes', 'ascii')) is py23_str
    assert _do_decoding(b'bytes', 'ascii') == 'bytes'
    assert _do_decoding(b'bytes', 'ascii') == b'bytes'.decode('ascii')


def test_args_to_enum_raises_TypeError_for_invalid_argument():
    with raises(TypeError):
        _args_to_enum(**{'alf': 0})


def test_args_to_enum_converts_signed_exp_float_to_ns_F():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': float,
                            'signed': True,
                            'exp': True}) == ns.F | ns.S


def test_args_to_enum_converts_signed_noexp_float_to_ns_FN():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': float,
                            'signed': True,
                            'exp': False}) == ns.F | ns.N | ns.S


def test_args_to_enum_converts_unsigned_exp_float_to_ns_FU():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': float,
                            'signed': False,
                            'exp': True}) == ns.F | ns.U
    # unsigned is default
    assert _args_to_enum(**{'number_type': float,
                            'signed': False,
                            'exp': True}) == ns.F


def test_args_to_enum_converts_unsigned_unexp_float_to_ns_FNU():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': float,
                            'signed': False,
                            'exp': False}) == ns.F | ns.U | ns.N


def test_args_to_enum_converts_float_and_path_and_py3safe_to_ns_FPT():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': float,
                            'as_path': True,
                            'py3_safe': True}) == ns.F | ns.P | ns.T


def test_args_to_enum_converts_int_and_path_to_ns_IP():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': int, 'as_path': True}) == ns.I | ns.P


def test_args_to_enum_converts_unsigned_int_and_py3safe_to_ns_IUT():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': int,
                            'signed': False,
                            'py3_safe': True}) == ns.I | ns.U | ns.T


def test_args_to_enum_converts_None_to_ns_IU():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(**{'number_type': None,
                            'exp': True}) == ns.I | ns.U

float_locale_group = (fast_float, True, True)
float_locale_nogroup = (fast_float, True, False)
float_nolocale_group = (fast_float, False, True)
float_nolocale_nogroup = (fast_float, False, False)
int_locale_group = (fast_int, True, True)
int_locale_nogroup = (fast_int, True, False)
int_nolocale_group = (fast_int, False, True)
int_nolocale_nogroup = (fast_int, False, False)


def test_fix_nan_converts_nan_to_negative_infinity_without_NANLAST():
    assert _fix_nan((float('nan'),), 0) == (float('-inf'),)
    assert _fix_nan(('a', 'b', float('nan')), 0) == ('a', 'b', float('-inf'))


def test_fix_nan_converts_nan_to_positive_infinity_with_NANLAST():
    assert _fix_nan((float('nan'),), ns.NANLAST) == (float('+inf'),)
    assert _fix_nan(('a', 'b', float('nan')), ns.NANLAST) == ('a', 'b', float('+inf'))


def test_chain_functions_is_a_no_op_if_no_functions_are_given():
    x = 2345
    assert chain_functions([])(x) is x


def test_chain_functions_combines_functions_in_given_order():
    x = 2345
    assert chain_functions([str, len, op_neg])(x) == -len(str(x))


def test_pre_split_function_is_no_op_for_no_alg_options_examples():
    x = 'feijGGAd'
    assert _pre_split_function(0)(x) is x


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_is_no_op_for_no_alg_options(x):
    assert _pre_split_function(0)(x) is x


def test_pre_split_function_performs_casefold_with_IGNORECASE_examples():
    x = 'feijGGAd'
    if sys.version_info[0:2] >= (3, 3):
        assert _pre_split_function(ns.IGNORECASE)(x) == x.casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE)(x) == x.lower()


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_performs_casefold_with_IGNORECASE(x):
    if sys.version_info[0:2] >= (3, 3):
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
    if sys.version_info[0:2] >= (3, 3):
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().lower()


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_pre_split_function_performs_swapcase_and_casefold_both_LOWERCASEFIRST_AND_IGNORECASE(x):
    if sys.version_info[0:2] >= (3, 3):
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().casefold()
    else:
        assert _pre_split_function(ns.IGNORECASE | ns.LOWERCASEFIRST)(x) == x.swapcase().lower()


def test_post_split_function_returns_fast_int_example():
    x = 'hello'
    assert _post_split_function(0)(x) is fast_int(x)
    assert _post_split_function(0)('5007') == fast_int('5007')


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text() | floats() | integers())
def test_post_split_function_returns_fast_int(x):
    assume(x)
    assert _post_split_function(0)(py23_str(x)) == fast_int(py23_str(x))


def test_post_split_function_with_FLOAT_returns_fast_float_example():
    x = 'hello'
    assert _post_split_function(ns.FLOAT)(x) is fast_float(x)
    assert _post_split_function(ns.FLOAT)('5007') == fast_float('5007')


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text() | floats() | integers())
def test_post_split_function_with_FLOAT_returns_fast_float(x):
    assume(x)
    assert _post_split_function(ns.FLOAT)(py23_str(x)) == fast_float(py23_str(x), nan=float('-inf'))


def test_post_split_function_with_FLOAT_returns_fast_float_with_neg_inf_replacing_nan():
    assert _post_split_function(ns.FLOAT)('nan') == fast_float('nan', nan=float('-inf'))


def test_post_split_function_with_FLOAT_and_NANLAST_returns_fast_float_with_pos_inf_replacing_nan():
    assert _post_split_function(ns.FLOAT | ns.NANLAST)('nan') == fast_float('nan', nan=float('+inf'))


def test_post_split_function_with_GROUPLETTERS_returns_fast_int_and_groupletters_example():
    x = 'hello'
    assert _post_split_function(ns.GROUPLETTERS)(x) == fast_int(x, key=groupletters)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_GROUPLETTERS_returns_fast_int_and_groupletters(x):
    assume(x)
    assert _post_split_function(ns.GROUPLETTERS)(x) == fast_int(x, key=groupletters)


def test_post_split_function_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _post_split_function(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert(groupletters(x)))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    try:
        assert _post_split_function(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert(groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise


def test_post_split_function_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _post_split_function(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert(groupletters(x)))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    try:
        assert _post_split_function(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert(groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise


def test_ungroupletters_with_empty_tuple_returns_double_empty_tuple():
    assert _ungroupletters((), '', '', 0) == ((), ())


def test_ungroupletters_with_null_string_first_element_adds_empty_string_on_first_tuple_element():
    assert _ungroupletters(('', 60), '', '', 0) == ((b'',) if use_pyicu else ('',), ('', 60))


def test_ungroupletters_returns_first_element_in_first_tuple_element_example():
    assert _ungroupletters(('this', 60), 'this60', '', 0) == (('t',), ('this', 60))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(x=text(), y=floats() | integers())
def test_ungroupletters_returns_first_element_in_first_tuple_element(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _ungroupletters((x, y), ''.join(map(py23_str, [x, y])), '', 0) == ((x[0],), (x, y))


def test_ungroupletters_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST_example():
    assert _ungroupletters(('this', 60), 'this60', '', ns._DUMB | ns.LOWERCASEFIRST) == (('T',), ('this', 60))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(x=text(), y=floats() | integers())
def test_ungroupletters_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _ungroupletters((x, y), ''.join(map(py23_str, [x, y])), '', ns._DUMB | ns.LOWERCASEFIRST) == ((x[0].swapcase(),), (x, y))


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_sep_inserter_does_nothing_if_no_numbers_example():
    assert list(_sep_inserter(iter(['a', 'b', 'c']), '')) == ['a', 'b', 'c']
    assert list(_sep_inserter(iter(['a']), '')) == ['a']


def test_sep_inserter_does_nothing_if_only_one_number_example():
    assert list(_sep_inserter(iter(['a', 5]), '')) == ['a', 5]


def test_sep_inserter_inserts_separator_string_between_two_numbers_example():
    assert list(_sep_inserter(iter([5, 9]), '')) == ['', 5, '', 9]
    assert list(_sep_inserter(iter([5, 9]), null_string)) == [null_string, 5, null_string, 9]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=text() | integers()))
def test_sep_inserter_inserts_separator_between_two_numbers(x):
    assume(bool(x))
    assert list(_sep_inserter(iter(x), '')) == list(add_leading_space_if_first_is_num(sep_inserter(x, ''), ''))


def test_path_splitter_splits_path_string_by_separator_example():
    z = '/this/is/a/path'
    assert _path_splitter(z) == tuple(pathlib.Path(z).parts)
    z = pathlib.Path('/this/is/a/path')
    assert _path_splitter(z) == tuple(pathlib.Path(z).parts)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(sampled_from(string.ascii_letters), min_size=2))
def test_path_splitter_splits_path_string_by_separator(x):
    assume(all(x))
    z = py23_str(pathlib.Path(*x))
    assert _path_splitter(z) == tuple(pathlib.Path(z).parts)


def test_path_splitter_splits_path_string_by_separator_and_removes_extension_example():
    z = '/this/is/a/path/file.exe'
    y = tuple(pathlib.Path(z).parts)
    assert _path_splitter(z) == y[:-1] + (pathlib.Path(z).stem, pathlib.Path(z).suffix)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(sampled_from(string.ascii_letters), min_size=3))
def test_path_splitter_splits_path_string_by_separator_and_removes_extension(x):
    assume(all(x))
    z = py23_str(pathlib.Path(*x[:-2])) + '.' + x[-1]
    y = tuple(pathlib.Path(z).parts)
    assert _path_splitter(z) == y[:-1] + (pathlib.Path(z).stem, pathlib.Path(z).suffix)


def test_number_extracter_raises_TypeError_if_given_a_number_example():
    with raises(TypeError):
        assert _number_extracter(50.0, _float_sign_exp_re, *float_nolocale_nogroup)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats())
def test_number_extracter_raises_TypeError_if_given_a_number(x):
    with raises(TypeError):
        assert _number_extracter(x, _float_sign_exp_re, *float_nolocale_nogroup)


def test_number_extracter_includes_plus_sign_and_exponent_in_float_definition_for_signed_exp_floats_example():
    assert _number_extracter('a5+5.034e-1', _float_sign_exp_re, *float_nolocale_nogroup) == ['a', 5.0, '', 0.5034]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_includes_plus_sign_and_exponent_in_float_definition_for_signed_exp_floats(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _number_extracter(s, _float_sign_exp_re, *float_nolocale_nogroup) == float_splitter(s, True, True, '')


def test_number_extracter_excludes_plus_sign_in_float_definition_but_includes_exponent_for_unsigned_exp_floats_example():
    assert _number_extracter('a5+5.034e-1', _float_nosign_exp_re, *float_nolocale_nogroup) == ['a', 5.0, '+', 0.5034]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_excludes_plus_sign_in_float_definition_but_includes_exponent_for_unsigned_exp_floats(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _number_extracter(s, _float_nosign_exp_re, *float_nolocale_nogroup) == float_splitter(s, False, True, '')


def test_number_extracter_includes_plus_and_minus_sign_in_float_definition_but_excludes_exponent_for_signed_noexp_floats_example():
    assert _number_extracter('a5+5.034e-1', _float_sign_noexp_re, *float_nolocale_nogroup) == ['a', 5.0, '', 5.034, 'e', -1.0]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_includes_plus_and_minus_sign_in_float_definition_but_excludes_exponent_for_signed_noexp_floats(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _number_extracter(s, _float_sign_noexp_re, *float_nolocale_nogroup) == float_splitter(s, True, False, '')


def test_number_extracter_excludes_plus_sign_and_exponent_in_float_definition_for_unsigned_noexp_floats_example():
    assert _number_extracter('a5+5.034e-1', _float_nosign_noexp_re, *float_nolocale_nogroup) == ['a', 5.0, '+', 5.034, 'e-', 1.0]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_excludes_plus_sign_and_exponent_in_float_definition_for_unsigned_noexp_floats(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _number_extracter(s, _float_nosign_noexp_re, *float_nolocale_nogroup) == float_splitter(s, False, False, '')


def test_number_extracter_excludes_plus_and_minus_sign_in_int_definition_for_unsigned_ints_example():
    assert _number_extracter('a5+5.034e-1', _int_nosign_re, *int_nolocale_nogroup) == ['a', 5, '+', 5, '.', 34, 'e-', 1]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
@example([10000000000000000000000000000000000000000000000000000000000000000000000000,
          100000000000000000000000000000000000000000000000000000000000000000000000000,
          100000000000000000000000000000000000000000000000000000000000000000000000000])
def test_number_extracter_excludes_plus_and_minus_sign_in_int_definition_for_unsigned_ints(x):
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _number_extracter(s, _int_nosign_re, *int_nolocale_nogroup) == int_splitter(s, False, '')


def test_number_extracter_includes_plus_and_minus_sign_in_int_definition_for_signed_ints_example():
    assert _number_extracter('a5+5.034e-1', _int_sign_re, *int_nolocale_nogroup) == ['a', 5, '', 5, '.', 34, 'e', -1]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_includes_plus_and_minus_sign_in_int_definition_for_signed_ints(x):
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _number_extracter(s, _int_sign_re, *int_nolocale_nogroup) == int_splitter(s, True, '')


def test_number_extracter_adds_leading_empty_string_if_input_begins_with_a_number_example():
    assert _number_extracter('6a5+5.034e-1', _float_sign_exp_re, *float_nolocale_nogroup) == ['', 6.0, 'a', 5.0, '', 0.5034]


def test_number_extracter_doubles_letters_with_lowercase_version_with_groupletters_for_float_example():
    assert _number_extracter('A5+5.034E-1', _float_sign_exp_re, *float_nolocale_group) == ['aA', 5.0, '', 0.5034]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_doubles_letters_with_lowercase_version_with_groupletters_for_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = float_splitter(s, True, True, '')
    t = [''.join([low(z) + z for z in y]) if type(y) != float else y for y in t]
    assert _number_extracter(s, _float_sign_exp_re, *float_nolocale_group) == t


def test_number_extracter_doubles_letters_with_lowercase_version_with_groupletters_for_int_example():
    assert _number_extracter('A5+5.034E-1', _int_nosign_re, *int_nolocale_group) == ['aA', 5, '++', 5, '..', 34, 'eE--', 1]


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_doubles_letters_with_lowercase_version_with_groupletters_for_int(x):
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = int_splitter(s, False, '')
    t = [''.join([low(z) + z for z in y]) if type(y) not in (int, long) else y for y in t]
    assert _number_extracter(s, _int_nosign_re, *int_nolocale_group) == t


def test_number_extracter_extracts_numbers_and_strxfrms_strings_with_use_locale_example():
    load_locale('en_US')
    strxfrm = get_strxfrm()
    assert _number_extracter('A5+5.034E-1', _int_nosign_re, *int_locale_nogroup) == [strxfrm('A'), 5, strxfrm('+'), 5, strxfrm('.'), 34, strxfrm('E-'), 1]
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_number_extracter_extracts_numbers_and_strxfrms_strings_with_use_locale(x):
    load_locale('en_US')
    assume(not any(any(i in bad_uni_chars for i in y) for y in x if isinstance(y, py23_str)))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = int_splitter(s, False, null_string)
    try:  # Account for locale bug on Python 3.2
        t = [y if i == 0 and y is null_string else locale_convert(y) if not isinstance(y, (float, long, int)) else y for i, y in enumerate(t)]
        assert _number_extracter(s, _int_nosign_re, *int_locale_nogroup) == t
    except OverflowError:
        pass
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test__natsort_key_with_nan_input_transforms_nan_to_negative_inf():
    assert _natsort_key('nan', None, ns.FLOAT) == ('', float('-inf'))
    assert _natsort_key(float('nan'), None, 0) == ('', float('-inf'))


def test__natsort_key_with_nan_input_and_NANLAST_transforms_nan_to_positive_inf():
    assert _natsort_key('nan', None, ns.FLOAT | ns.NANLAST) == ('', float('+inf'))
    assert _natsort_key(float('nan'), None, ns.NANLAST) == ('', float('+inf'))
    assert ns.NL == ns.NANLAST


# The remaining tests provide no examples, just hypothesis tests.
# They only confirm that _natsort_key uses the above building blocks.


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_float_and_signed_splits_input_into_string_and_signed_float_with_exponent(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert ns.F == ns.FLOAT
    assert ns.S == ns.SIGNED
    assert _natsort_key(s, None, ns.F | ns.S) == tuple(_number_extracter(s, _float_sign_exp_re, *float_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_real_splits_input_into_string_and_signed_float_with_exponent(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert ns.R == ns.F | ns.S
    assert _natsort_key(s, None, ns.R) == tuple(_number_extracter(s, _float_sign_exp_re, *float_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_real_matches_signed_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, ns.R) == _natsort_key(s, None, ns.F | ns.S)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_float_and_signed_and_noexp_splits_input_into_string_and_signed_float_without_exponent(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert ns.N == ns.NOEXP
    assert _natsort_key(s, None, ns.F | ns.S | ns.N) == tuple(_number_extracter(s, _float_sign_noexp_re, *float_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_float_and_unsigned_splits_input_into_string_and_unsigned_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert ns.U == ns.UNSIGNED
    assert _natsort_key(s, None, ns.F | ns.U) == tuple(_number_extracter(s, _float_nosign_exp_re, *float_nolocale_nogroup))
    # Default is unsigned search
    assert _natsort_key(s, None, ns.F) == tuple(_number_extracter(s, _float_nosign_exp_re, *float_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_float_and_noexp_splits_input_into_string_and_unsigned_float_without_exponent(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, ns.F | ns.N) == tuple(_number_extracter(s, _float_nosign_noexp_re, *float_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_int_splits_input_into_string_and_unsigned_int(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert ns.I == ns.INT
    assert _natsort_key(s, None, ns.INT) == tuple(_number_extracter(s, _int_nosign_re, *int_nolocale_nogroup))
    # Default is int search
    assert _natsort_key(s, None, ns.NOEXP) == tuple(_number_extracter(s, _int_nosign_re, *int_nolocale_nogroup))
    # NOEXP is ignored for integers
    assert _natsort_key(s, None, ns.I | ns.NOEXP) == tuple(_number_extracter(s, _int_nosign_re, *int_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_int_splits_and_signed_input_into_string_and_signed_int(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, ns.INT | ns.SIGNED) == tuple(_number_extracter(s, _int_sign_re, *int_nolocale_nogroup))
    assert _natsort_key(s, None, ns.SIGNED) == tuple(_number_extracter(s, _int_sign_re, *int_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_version_or_digit_matches_usigned_int(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, ns.VERSION) == _natsort_key(s, None, ns.INT | ns.UNSIGNED)
    assert _natsort_key(s, None, ns.DIGIT) == _natsort_key(s, None, ns.VERSION)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_key_applies_key_function_before_splitting(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, lambda x: x.upper(), ns.I) == tuple(_number_extracter(s.upper(), _int_nosign_re, *int_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_tuple_input_returns_nested_tuples(x):
    # Iterables are parsed recursively so you can sort lists of lists.
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = tuple(_number_extracter(s, _int_nosign_re, *int_nolocale_nogroup))
    assert _natsort_key((s, s), None, ns.I) == (t, t)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_tuple_input_but_itemgetter_key_returns_split_second_element(x):
    # A key is applied before recursion, but not in the recursive calls.
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = tuple(_number_extracter(s, _int_nosign_re, *int_nolocale_nogroup))
    assert _natsort_key((s, s), itemgetter(1), ns.I) == t


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats())
def test__natsort_key_with_numeric_input_returns_number_with_leading_empty_string(x):
    assume(not isnan(x))
    if x.is_integer():
        x = int(x)
    assert _natsort_key(x, None, ns.I) == ('', x)


def test__natsort_key_with_invalid_alg_input_raises_ValueError():
    # Invalid arguments give the correct response
    with raises(ValueError) as err:
        _natsort_key('a', None, '1')
    assert str(err.value) == "_natsort_key: 'alg' argument must be from the enum 'ns', got 1"


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_IGNORECASE_lowercases_text(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    try:
        assert _natsort_key(s, None, ns.IGNORECASE) == tuple(_number_extracter(s.casefold(), _int_nosign_re, *int_nolocale_nogroup))
    except AttributeError:
        assert _natsort_key(s, None, ns.IGNORECASE) == tuple(_number_extracter(s.lower(), _int_nosign_re, *int_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_LOWERCASEFIRST_inverts_text_case(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, ns.LOWERCASEFIRST) == tuple(_number_extracter(s.swapcase(), _int_nosign_re, *int_nolocale_nogroup))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_GROUPLETTERS_doubles_text_with_lowercase_letter_first(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(ichain([repr(y)] if type(y) in (float, long, int) else [low(y), y] for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = _number_extracter(s, _int_nosign_re, *int_nolocale_nogroup)
    assert _natsort_key(s, None, ns.GROUPLETTERS) == tuple(''.join(low(z) + z for z in y) if type(y) not in (float, long, int) else y for y in t)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_GROUPLETTERS_and_LOWERCASEFIRST_inverts_text_first_then_doubles_letters_with_lowercase_letter_first(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(ichain([repr(y)] if type(y) in (float, long, int) else [low(y), y] for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    t = _number_extracter(s.swapcase(), _int_nosign_re, *int_nolocale_nogroup)
    assert _natsort_key(s, None, ns.G | ns.LF) == tuple(''.join(low(z) + z for z in y) if type(y) not in (float, long, int) else y for y in t)


def test__natsort_key_with_bytes_input_only_applies_LOWERCASEFIRST_or_IGNORECASE_and_returns_in_tuple():
    if sys.version[0] == '3':
        assert _natsort_key(b'Apple56', None, ns.I) == (b'Apple56',)
        assert _natsort_key(b'Apple56', None, ns.LF) == (b'aPPLE56',)
        assert _natsort_key(b'Apple56', None, ns.IC) == (b'apple56',)
        assert _natsort_key(b'Apple56', None, ns.G) == (b'Apple56',)
    else:
        assert True


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_LOCALE_transforms_floats_according_to_the_current_locale_and_strxfrms_strings(x):
    # Locale aware sorting
    assume(not any(type(y) == float and isnan(y) for y in x))
    assume(not any(any(i in bad_uni_chars for i in y) for y in x if isinstance(y, py23_str)))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    load_locale('en_US')
    if dumb_sort():
        assert _natsort_key(s, None, ns.LOCALE | ns.F) == tuple(_number_extracter(s.swapcase(), _float_nosign_exp_re, *float_locale_group))
    else:
        assert _natsort_key(s, None, ns.LOCALE | ns.F) == tuple(_number_extracter(s, _float_nosign_exp_re, *float_locale_nogroup))
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_LOCALE_and_UNGROUPLETTERS_places_space_before_string_with_capital_first_letter(x):
    # Locale aware sorting
    assume(not any(type(y) == float and isnan(y) for y in x))
    assume(not any(any(i in bad_uni_chars for i in y) for y in x if isinstance(y, py23_str)))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    load_locale('en_US')
    if dumb_sort():
        t = tuple(_number_extracter(s.swapcase(), _float_nosign_exp_re, *float_locale_group))
    else:
        t = tuple(_number_extracter(s, _float_nosign_exp_re, *float_locale_nogroup))
    if not t:
        r = (t, t)
    elif t[0] in (null_string, get_strxfrm()(b'\x00') if sys.version[0] == '2' and not use_pyicu else null_string):
        r = ((b'' if use_pyicu else '',), t)
    else:
        r = ((s[0],), t)
    assert _natsort_key(s, None, ns.LOCALE | ns.UNGROUPLETTERS | ns.F) == r
    # The below are all aliases for UNGROUPLETTERS
    assert ns.UNGROUPLETTERS == ns.UG
    assert ns.UNGROUPLETTERS == ns.CAPITALFIRST
    assert ns.UNGROUPLETTERS == ns.C
    locale.setlocale(locale.LC_NUMERIC, str(''))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_UNGROUPLETTERS_does_nothing_without_LOCALE(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, ns.UG | ns.I) == _natsort_key(s, None, ns.I)


# It is difficult to generate code that will create random filesystem paths,
# so "example" based tests are given for the PATH option.


def test__natsort_key_with_absolute_path_intput_and_PATH_returns_nested_tuple_where_each_element_is_path_component_with_leading_root_and_split_extensions():
    # Turn on PATH to split a file path into components
    assert _natsort_key('/p/Folder (10)/file34.5nm (2).tar.gz', None, ns.PATH | ns.F) == (('/',), ('p', ), ('Folder (', 10.0, ')',), ('file', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_relative_path_intput_and_PATH_returns_nested_tuple_where_each_element_is_path_component_with_leading_relative_parent_and_split_extensions():
    assert _natsort_key('../Folder (10)/file (2).tar.gz', None, ns.PATH | ns.F) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_relative_path_intput_and_PATH_returns_nested_tuple_where_each_element_is_path_component_and_split_extensions():
    assert _natsort_key('Folder (10)/file.f34.5nm (2).tar.gz', None, ns.PATH | ns.F) == (('Folder (', 10.0, ')',), ('file.f', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_pathlib_intput_and_PATH_returns_nested_tuples():
    # Converts pathlib PurePath (and subclass) objects to string before sorting
    assert _natsort_key(pathlib.Path('../Folder (10)/file (2).tar.gz'), None, ns.PATH | ns.F) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_numeric_input_and_PATH_returns_number_in_nested_tuple():
    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    assert _natsort_key(10, None, ns.PATH) == (('', 10),)


def test__natsort_key_with_tuple_of_paths_and_PATH_returns_triply_nested_tuple():
    # PATH also handles recursion well.
    assert _natsort_key(('/Folder', '/Folder (1)'), None, ns.PATH) == ((('/',), ('Folder',)), (('/',), ('Folder (', 1, ')')))
