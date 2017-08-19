# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

import pathlib
import string
from itertools import chain
from operator import neg as op_neg
from pytest import raises
from natsort.ns_enum import ns
from natsort.utils import (
    _sep_inserter,
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
    _groupletters,
    chain_functions,
)
from natsort.compat.py23 import py23_str
from natsort.compat.locale import null_string
from slow_splitters import (
    sep_inserter,
    add_leading_space_if_first_is_num,
)
from compat.locale import low
from hypothesis import (
    assume,
    given,
)
from hypothesis.strategies import (
    sampled_from,
    lists,
    text,
    integers,
)


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
    assert ns.LOCALEALPHA == ns.LA
    assert ns.LOCALENUM == ns.LN
    assert ns.LOCALE == ns.L
    assert ns.IGNORECASE == ns.IC
    assert ns.LOWERCASEFIRST == ns.LF
    assert ns.GROUPLETTERS == ns.G
    assert ns.UNGROUPLETTERS == ns.UG
    assert ns.CAPITALFIRST == ns.C
    assert ns.UNGROUPLETTERS == ns.CAPITALFIRST
    assert ns.NANLAST == ns.NL
    assert ns.COMPATIBILITYNORMALIZE == ns.CN

    # Convenience
    assert ns.LOCALE == ns.LOCALEALPHA | ns.LOCALENUM
    assert ns.REAL == ns.FLOAT | ns.SIGNED
    assert ns._NUMERIC_ONLY == ns.REAL | ns.NOEXP


def test_chain_functions_is_a_no_op_if_no_functions_are_given():
    x = 2345
    assert chain_functions([])(x) is x


def test_chain_functions_does_one_function_if_one_function_is_given():
    x = '2345'
    assert chain_functions([len])(x) == 4


def test_chain_functions_combines_functions_in_given_order():
    x = 2345
    assert chain_functions([str, len, op_neg])(x) == -len(str(x))


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.

def test_groupletters_returns_letters_with_lowercase_transform_of_letter_example():
    assert _groupletters('HELLO') == 'hHeElLlLoO'
    assert _groupletters('hello') == 'hheelllloo'


@given(text())
def test_groupeletters_returns_letters_with_lowercase_transform_of_letter(x):
    assume(bool(x))
    assert _groupletters(x) == ''.join(chain.from_iterable([low(y), y] for y in x))


def test_sep_inserter_does_nothing_if_no_numbers_example():
    assert list(_sep_inserter(iter(['a', 'b', 'c']), '')) == ['a', 'b', 'c']
    assert list(_sep_inserter(iter(['a']), '')) == ['a']


def test_sep_inserter_does_nothing_if_only_one_number_example():
    assert list(_sep_inserter(iter(['a', 5]), '')) == ['a', 5]


def test_sep_inserter_inserts_separator_string_between_two_numbers_example():
    assert list(_sep_inserter(iter([5, 9]), '')) == ['', 5, '', 9]
    assert list(_sep_inserter(iter([5, 9]), null_string)) == [null_string, 5, null_string, 9]


@given(lists(elements=text() | integers()))
def test_sep_inserter_inserts_separator_between_two_numbers(x):
    assume(bool(x))
    assert list(_sep_inserter(iter(x), '')) == list(add_leading_space_if_first_is_num(sep_inserter(x, ''), ''))


def test_path_splitter_splits_path_string_by_separator_example():
    z = '/this/is/a/path'
    assert tuple(_path_splitter(z)) == tuple(pathlib.Path(z).parts)
    z = pathlib.Path('/this/is/a/path')
    assert tuple(_path_splitter(z)) == tuple(pathlib.Path(z).parts)


@given(lists(sampled_from(string.ascii_letters), min_size=2))
def test_path_splitter_splits_path_string_by_separator(x):
    assume(all(x))
    z = py23_str(pathlib.Path(*x))
    assert tuple(_path_splitter(z)) == tuple(pathlib.Path(z).parts)


def test_path_splitter_splits_path_string_by_separator_and_removes_extension_example():
    z = '/this/is/a/path/file.exe'
    y = tuple(pathlib.Path(z).parts)
    assert tuple(_path_splitter(z)) == y[:-1] + (pathlib.Path(z).stem, pathlib.Path(z).suffix)


@given(lists(sampled_from(string.ascii_letters), min_size=3))
def test_path_splitter_splits_path_string_by_separator_and_removes_extension(x):
    assume(all(x))
    z = py23_str(pathlib.Path(*x[:-2])) + '.' + x[-1]
    y = tuple(pathlib.Path(z).parts)
    assert tuple(_path_splitter(z)) == y[:-1] + (pathlib.Path(z).stem, pathlib.Path(z).suffix)
