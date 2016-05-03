# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import sys
import pathlib
import pytest
import string
from math import isnan, isinf
from operator import neg as op_neg
from pytest import raises
from natsort.ns_enum import ns
from natsort.utils import (
    _sep_inserter,
    _natsort_key,
    _args_to_enum,
    _regex_chooser,
    _float_sign_exp_re,
    _float_nosign_exp_re,
    _float_sign_noexp_re,
    _float_nosign_noexp_re,
    _int_nosign_re,
    _int_sign_re,
    _do_decoding,
    _path_splitter,
    chain_functions,
    _parse_string_function,
    _parse_path_function,
    _parse_number_function,
    _parse_bytes_function,
    _pre_split_function,
    _post_split_function,
    _post_string_parse_function,
)
from natsort.locale_help import (
    locale_convert_function,
    groupletters,
)
from natsort.compat.py23 import py23_str
from natsort.compat.locale import (
    use_pyicu,
    null_string,
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
from compat.hypothesis import (
    assume,
    given,
    example,
    sampled_from,
    lists,
    text,
    floats,
    integers,
    binary,
    use_hypothesis,
)
from compat.locale import bad_uni_chars

if sys.version[0] == '3':
    long = int


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


def test_regex_chooser_returns_correct_regular_expression_object():
    assert _regex_chooser[ns.INT] is _int_nosign_re
    assert _regex_chooser[ns.INT | ns.NOEXP] is _int_nosign_re
    assert _regex_chooser[ns.INT | ns.SIGNED] is _int_sign_re
    assert _regex_chooser[ns.INT | ns.SIGNED | ns.NOEXP] is _int_sign_re
    assert _regex_chooser[ns.FLOAT] is _float_nosign_exp_re
    assert _regex_chooser[ns.FLOAT | ns.NOEXP] is _float_nosign_noexp_re
    assert _regex_chooser[ns.FLOAT | ns.SIGNED] is _float_sign_exp_re
    assert _regex_chooser[ns.FLOAT | ns.SIGNED | ns.NOEXP] is _float_sign_noexp_re


def test_ns_enum_values_have_are_as_expected():
    # Defaults
    assert ns.TYPESAFE == 0
    assert ns.INT == 0
    assert ns.VERSION == 0
    assert ns.DIGIT == 0
    assert ns.UNSIGNED == 0

    # Aliases
    assert ns.TYPESAFE == ns.T
    assert ns.INT == ns.I
    assert ns.VERSION == ns.V
    assert ns.DIGIT == ns.D
    assert ns.UNSIGNED == ns.U
    assert ns.FLOAT == ns.F
    assert ns.SIGNED == ns.S
    assert ns.NOEXP == ns.N
    assert ns.PATH == ns.P
    assert ns.LOCALE == ns.L
    assert ns.IGNORECASE == ns.IC
    assert ns.LOWERCASEFIRST == ns.LF
    assert ns.GROUPLETTERS == ns.G
    assert ns.UNGROUPLETTERS == ns.UG
    assert ns.CAPITALFIRST == ns.C
    assert ns.UNGROUPLETTERS == ns.CAPITALFIRST
    assert ns.NANLAST == ns.NL

    # Convenience
    assert ns.REAL == ns.FLOAT | ns.SIGNED
    assert ns._NUMERIC_ONLY == ns.REAL | ns.NOEXP


def test_chain_functions_is_a_no_op_if_no_functions_are_given():
    x = 2345
    assert chain_functions([])(x) is x


def test_chain_functions_combines_functions_in_given_order():
    x = 2345
    assert chain_functions([str, len, op_neg])(x) == -len(str(x))


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


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


def test_post_split_function_with_LOCALE_returns_fast_int_and_groupletters_example():
    x = 'hello'
    assert _post_split_function(ns.LOCALE)(x) == fast_int(x, key=locale_convert_function())


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_returns_fast_int_and_groupletters(x):
    assume(x)
    assume(not any(y in bad_uni_chars for y in x))
    assert _post_split_function(ns.LOCALE)(x) == fast_int(x, key=locale_convert_function())


def test_post_split_function_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _post_split_function(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert_function()(groupletters(x)))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_and_GROUPLETTERS_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    try:
        assert _post_split_function(ns.GROUPLETTERS | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert_function()(groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise


def test_post_split_function_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert_example():
    x = 'hello'
    assert _post_split_function(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert_function()(groupletters(x)))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_split_function_with_LOCALE_and_DUMB_returns_fast_int_and_groupletters_and_locale_convert(x):
    assume(x)
    try:
        assert _post_split_function(ns._DUMB | ns.LOCALE)(x) == fast_int(x, key=lambda x: locale_convert_function()(groupletters(x)))
    except ValueError as e:  # handle broken locale lib on BSD.
        if 'is not in range' not in str(e):
            raise


def test_post_string_parse_function_with_iterable_returns_tuple_with_no_options_example():
    assert _post_string_parse_function(0, '')(iter([7]), '') == (7, )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test_post_string_parse_function_with_iterable_returns_tuple_with_no_options(x):
    assert _post_string_parse_function(0, '')(iter([x]), '') == (x, )


def test_post_string_parse_function_with_empty_tuple_returns_double_empty_tuple():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')((), '') == ((), ())


def test_post_string_parse_function_with_null_string_first_element_adds_empty_string_on_first_tuple_element():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')(('', 60), '') == ((b'',) if use_pyicu else ('',), ('', 60))


def test_post_string_parse_function_returns_first_element_in_first_tuple_element_example():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')(('this', 60), 'this60') == (('t',), ('this', 60))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(x=text(), y=floats() | integers())
def test_post_string_parse_function_returns_first_element_in_first_tuple_element(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS, '')((x, y), ''.join(map(py23_str, [x, y]))) == ((x[0],), (x, y))


def test_post_string_parse_function_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST_example():
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS | ns._DUMB | ns.LOWERCASEFIRST, '')(('this', 60), 'this60') == (('T',), ('this', 60))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(x=text(), y=floats() | integers())
def test_post_string_parse_function_returns_first_element_in_first_tuple_element_caseswapped_with_DUMB_and_LOWERCASEFIRST(x, y):
    assume(x)
    assume(not isnan(y))
    assume(not isinf(y))
    assert _post_string_parse_function(ns.LOCALE | ns.UNGROUPLETTERS | ns._DUMB | ns.LOWERCASEFIRST, '')((x, y), ''.join(map(py23_str, [x, y]))) == ((x[0].swapcase(),), (x, y))


def test_parse_number_function_makes_function_that_returns_tuple_example():
    assert _parse_number_function(0, '')(57) == ('', 57)
    assert _parse_number_function(0, '')(float('nan')) == ('', float('-inf'))
    assert _parse_number_function(ns.NANLAST, '')(float('nan')) == ('', float('+inf'))


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test_parse_number_function_makes_function_that_returns_tuple(x):
    assume(not isnan(x))
    assert _parse_number_function(0, '')(x) == ('', x)


def test_parse_number_function_with_PATH_makes_function_that_returns_nested_tuple_example():
    assert _parse_number_function(ns.PATH, '')(57) == (('', 57), )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test_parse_number_function_with_PATH_makes_function_that_returns_nested_tuple(x):
    assume(not isnan(x))
    assert _parse_number_function(ns.PATH, '')(x) == (('', x), )


def test_parse_bytes_function_makes_function_that_returns_tuple_example():
    assert _parse_bytes_function(0)(b'hello') == (b'hello', )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(binary())
def test_parse_bytes_function_makes_function_that_returns_tuple(x):
    assert _parse_bytes_function(0)(x) == (x, )


def test_parse_bytes_function_with_IGNORECASE_makes_function_that_returns_tuple_with_lowercase_example():
    assert _parse_bytes_function(ns.IGNORECASE)(b'HelLo') == (b'hello', )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(binary())
def test_parse_bytes_function_with_IGNORECASE_makes_function_that_returns_tuple_with_lowercase(x):
    assert _parse_bytes_function(ns.IGNORECASE)(x) == (x.lower(), )


def test_parse_bytes_function_with_PATH_makes_function_that_returns_nested_tuple_example():
    assert _parse_bytes_function(ns.PATH)(b'hello') == ((b'hello', ), )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(binary())
def test_parse_bytes_function_with_PATH_makes_function_that_returns_nested_tuple(x):
    assert _parse_bytes_function(ns.PATH)(x) == ((x, ), )


def test_parse_bytes_function_with_PATH_and_IGNORECASE_makes_function_that_returns_nested_tuple_with_lowercase_example():
    assert _parse_bytes_function(ns.PATH | ns.IGNORECASE)(b'HelLo') == ((b'hello', ), )


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(binary())
def test_parse_bytes_function_with_PATH_and_IGNORECASE_makes_function_that_returns_nested_tuple_with_lowercase(x):
    assert _parse_bytes_function(ns.PATH | ns.IGNORECASE)(x) == ((x.lower(), ), )


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
    assert tuple(_path_splitter(z)) == tuple(pathlib.Path(z).parts)
    z = pathlib.Path('/this/is/a/path')
    assert tuple(_path_splitter(z)) == tuple(pathlib.Path(z).parts)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(sampled_from(string.ascii_letters), min_size=2))
def test_path_splitter_splits_path_string_by_separator(x):
    assume(all(x))
    z = py23_str(pathlib.Path(*x))
    assert tuple(_path_splitter(z)) == tuple(pathlib.Path(z).parts)


def test_path_splitter_splits_path_string_by_separator_and_removes_extension_example():
    z = '/this/is/a/path/file.exe'
    y = tuple(pathlib.Path(z).parts)
    assert tuple(_path_splitter(z)) == y[:-1] + (pathlib.Path(z).stem, pathlib.Path(z).suffix)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(sampled_from(string.ascii_letters), min_size=3))
def test_path_splitter_splits_path_string_by_separator_and_removes_extension(x):
    assume(all(x))
    z = py23_str(pathlib.Path(*x[:-2])) + '.' + x[-1]
    y = tuple(pathlib.Path(z).parts)
    assert tuple(_path_splitter(z)) == y[:-1] + (pathlib.Path(z).stem, pathlib.Path(z).suffix)


def no_op(x):
    """A function that does nothing."""
    return x


def tuple2(x, dummy):
    """Make the input a tuple."""
    return tuple(x)


def test_parse_string_function_raises_TypeError_if_given_a_number_example():
    with raises(TypeError):
        assert _parse_string_function(0, '', _float_sign_exp_re.split, no_op, fast_float, tuple2)(50.0)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats())
def test_parse_string_function_raises_TypeError_if_given_a_number(x):
    with raises(TypeError):
        assert _parse_string_function(0, '', _float_sign_exp_re.split, no_op, fast_float, tuple2)(x)


def test_parse_string_function_only_parses_digits_with_nosign_int_example():
    assert _parse_string_function(0, '', _int_nosign_re.split, no_op, fast_int, tuple2)('a5+5.034e-1') == ('a', 5, '+', 5, '.', 34, 'e-', 1)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
@example([10000000000000000000000000000000000000000000000000000000000000000000000000,
          100000000000000000000000000000000000000000000000000000000000000000000000000,
          100000000000000000000000000000000000000000000000000000000000000000000000000])
def test_parse_string_function_only_parses_digits_with_nosign_int(x):
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_function(0, '', _int_nosign_re.split, no_op, fast_int, tuple2)(s) == int_splitter(s, False, '')


def test_parse_string_function_parses_digit_with_sign_with_signed_int_example():
    assert _parse_string_function(0, '', _int_sign_re.split, no_op, fast_int, tuple2)('a5+5.034e-1') == ('a', 5, '', 5, '.', 34, 'e', -1)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_parse_string_function_parses_digit_with_sign_with_signed_int(x):
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_function(0, '', _int_sign_re.split, no_op, fast_int, tuple2)(s) == int_splitter(s, True, '')


def test_parse_string_function_only_parses_float_with_nosign_noexp_float_example():
    assert _parse_string_function(0, '', _float_nosign_noexp_re.split, no_op, fast_float, tuple2)('a5+5.034e-1') == ('a', 5.0, '+', 5.034, 'e-', 1.0)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_parse_string_function_only_parses_float_with_nosign_noexp_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_function(0, '', _float_nosign_noexp_re.split, no_op, fast_float, tuple2)(s) == float_splitter(s, False, False, '')


def test_parse_string_function_only_parses_float_with_exponent_with_nosign_exp_float_example():
    assert _parse_string_function(0, '', _float_nosign_exp_re.split, no_op, fast_float, tuple2)('a5+5.034e-1') == ('a', 5.0, '+', 0.5034)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_parse_string_function_only_parses_float_with_exponent_with_nosign_exp_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_function(0, '', _float_nosign_exp_re.split, no_op, fast_float, tuple2)(s) == float_splitter(s, False, True, '')


def test_parse_string_function_only_parses_float_with_sign_with_sign_noexp_float_example():
    assert _parse_string_function(0, '', _float_sign_noexp_re.split, no_op, fast_float, tuple2)('a5+5.034e-1') == ('a', 5.0, '', 5.034, 'e', -1.0)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_parse_string_function_only_parses_float_with_sign_with_sign_noexp_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_function(0, '', _float_sign_noexp_re.split, no_op, fast_float, tuple2)(s) == float_splitter(s, True, False, '')


def test_parse_string_function_parses_float_with_sign_exp_float_example():
    assert _parse_string_function(0, '', _float_sign_exp_re.split, no_op, fast_float, tuple2)('a5+5.034e-1') == ('a', 5.0, '', 0.5034)
    assert _parse_string_function(0, '', _float_sign_exp_re.split, no_op, fast_float, tuple2)('6a5+5.034e-1') == ('', 6.0, 'a', 5.0, '', 0.5034)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test_parse_string_function_parses_float_with_sign_exp_float(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_function(0, '', _float_sign_exp_re.split, no_op, fast_float, tuple2)(s) == float_splitter(s, True, True, '')


def test_parse_string_function_selects_pre_function_value_if_not_dumb():
    def tuple2(x, orig):
        """Make the input a tuple."""
        return (orig[0], tuple(x))
    assert _parse_string_function(0, '', _int_nosign_re.split, str.upper, fast_float, tuple2)('a5+5.034e-1') == ('A', ('A', 5, '+', 5, '.', 34, 'E-', 1))
    assert _parse_string_function(ns._DUMB, '', _int_nosign_re.split, str.upper, fast_float, tuple2)('a5+5.034e-1') == ('A', ('A', 5, '+', 5, '.', 34, 'E-', 1))
    assert _parse_string_function(ns.LOCALE, '', _int_nosign_re.split, str.upper, fast_float, tuple2)('a5+5.034e-1') == ('A', ('A', 5, '+', 5, '.', 34, 'E-', 1))
    assert _parse_string_function(ns.LOCALE | ns._DUMB, '', _int_nosign_re.split, str.upper, fast_float, tuple2)('a5+5.034e-1') == ('a', ('A', 5, '+', 5, '.', 34, 'E-', 1))


def test_parse_path_function_parses_string_as_path_then_as_string():
    splt = _parse_string_function(0, '', _float_sign_exp_re.split, no_op, fast_float, tuple2)
    assert _parse_path_function(splt)('/p/Folder (10)/file34.5nm (2).tar.gz') == (('/',), ('p', ), ('Folder (', 10.0, ')',), ('file', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))
    assert _parse_path_function(splt)('../Folder (10)/file (2).tar.gz') == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))
    assert _parse_path_function(splt)('Folder (10)/file.f34.5nm (2).tar.gz') == (('Folder (', 10.0, ')',), ('file.f', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))


# Just a few tests to make sure _natsort_key is working

regex = _regex_chooser[ns.INT]
pre = _pre_split_function(ns.INT)
post = _post_split_function(ns.INT)
after = _post_string_parse_function(ns.INT, '')
string_func = _parse_string_function(ns.INT, '', regex.split, pre, post, after)
bytes_func = _parse_bytes_function(ns.INT)
num_func = _parse_number_function(ns.INT, '')


def test__natsort_key_with_numeric_input_and_PATH_returns_number_in_nested_tuple():
    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    sfunc = _parse_path_function(string_func)
    bytes_func = _parse_bytes_function(ns.PATH)
    num_func = _parse_number_function(ns.PATH, '')
    assert _natsort_key(10, None, sfunc, bytes_func, num_func) == (('', 10),)


def test__natsort_key_with_bytes_input_and_PATH_returns_number_in_nested_tuple():
    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    sfunc = _parse_path_function(string_func)
    bytes_func = _parse_bytes_function(ns.PATH)
    num_func = _parse_number_function(ns.PATH, '')
    assert _natsort_key(b'/hello/world', None, sfunc, bytes_func, num_func) == ((b'/hello/world',),)


def test__natsort_key_with_tuple_of_paths_and_PATH_returns_triply_nested_tuple():
    # PATH also handles recursion well.
    sfunc = _parse_path_function(string_func)
    bytes_func = _parse_bytes_function(ns.PATH)
    num_func = _parse_number_function(ns.PATH, '')
    assert _natsort_key(('/Folder', '/Folder (1)'), None, sfunc, bytes_func, num_func) == ((('/',), ('Folder',)), (('/',), ('Folder (', 1, ')')))


# The remaining tests provide no examples, just hypothesis tests.
# They only confirm that _natsort_key uses the above building blocks.


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(floats() | integers())
def test__natsort_key_with_numeric_input_takes_number_path(x):
    assume(not isnan(x))
    assert _natsort_key(x, None, string_func, bytes_func, num_func) == num_func(x)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(binary())
def test__natsort_key_with_bytes_input_takes_bytes_path(x):
    assert _natsort_key(x, None, string_func, bytes_func, num_func) == bytes_func(x)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=floats() | text() | integers(), min_size=1, max_size=10))
def test__natsort_key_with_text_input_takes_string_path(x):
    assume(not any(type(y) == float and isnan(y) for y in x))
    s = ''.join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _natsort_key(s, None, string_func, bytes_func, num_func) == string_func(s)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(lists(elements=text(), min_size=1, max_size=10))
def test__natsort_key_with_nested_input_takes_nested_path(x):
    assert _natsort_key(x, None, string_func, bytes_func, num_func) == tuple(string_func(s) for s in x)


@pytest.mark.skipif(not use_hypothesis, reason='requires python2.7 or greater')
@given(text())
def test__natsort_key_with_key_argument_applies_key_before_processing(x):
    assert _natsort_key(x, len, string_func, bytes_func, num_func) == num_func(len(x))
