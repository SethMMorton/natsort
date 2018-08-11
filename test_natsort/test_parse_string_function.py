# -*- coding: utf-8 -*-
"""These test the utils.py functions."""
from __future__ import unicode_literals

from hypothesis import example, given
from hypothesis.strategies import floats, integers, lists, text
from natsort.compat.fastnumbers import fast_float, fast_int
from natsort.compat.py23 import PY_VERSION, py23_str
from natsort.ns_enum import ns, ns_DUMB
from natsort.utils import NumericalRegularExpressions as nre
from natsort.utils import _parse_path_factory, _parse_string_factory
from pytest import raises

from slow_splitters import float_splitter, int_splitter

if PY_VERSION >= 3:
    long = int


def whitespace_check(x):
    """Simplifies testing"""
    try:
        if x.isspace():
            return x in " \t\n\r\f\v"
        else:
            return True
    except (AttributeError, TypeError):
        return True


def no_op(x):
    """A function that does nothing."""
    return x


def tuple2(x, dummy):
    """Make the input a tuple."""
    return tuple(x)


# Each test has an "example" version for demonstrative purposes,
# and a test that uses the hypothesis module.


def test_parse_string_factory_raises_TypeError_if_given_a_number_example():
    with raises(TypeError):
        assert _parse_string_factory(
            0, "", nre.float_sign_exp().split, no_op, fast_float, tuple2
        )(50.0)


@given(floats())
def test_parse_string_factory_raises_TypeError_if_given_a_number(x):
    with raises(TypeError):
        assert _parse_string_factory(
            0, "", nre.float_sign_exp().split, no_op, fast_float, tuple2
        )(x)


def test_parse_string_factory_only_parses_digits_with_nosign_int_example():
    assert _parse_string_factory(
        0, "", nre.int_nosign().split, no_op, fast_int, tuple2
    )("a5+5.034e-1") == ("a", 5, "+", 5, ".", 34, "e-", 1)


@given(
    lists(
        elements=floats() | text().filter(whitespace_check) | integers(),
        min_size=1,
        max_size=10,
    )
)
@example(
    [
        10000000000000000000000000000000000000000000000000000000000000000000000000,
        100000000000000000000000000000000000000000000000000000000000000000000000000,
        100000000000000000000000000000000000000000000000000000000000000000000000000,
    ]
)
def test_parse_string_factory_only_parses_digits_with_nosign_int(x):
    s = "".join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_factory(
        0, "", nre.int_nosign().split, no_op, fast_int, tuple2
    )(s) == int_splitter(s, False, "")


def test_parse_string_factory_parses_digit_with_sign_with_signed_int_example():
    assert _parse_string_factory(0, "", nre.int_sign().split, no_op, fast_int, tuple2)(
        "a5+5.034e-1"
    ) == ("a", 5, "", 5, ".", 34, "e", -1)


@given(
    lists(
        elements=floats() | text().filter(whitespace_check) | integers(),
        min_size=1,
        max_size=10,
    )
)
def test_parse_string_factory_parses_digit_with_sign_with_signed_int(x):
    s = "".join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_factory(0, "", nre.int_sign().split, no_op, fast_int, tuple2)(
        s
    ) == int_splitter(s, True, "")


def test_parse_string_factory_only_parses_float_with_nosign_noexp_float_example():
    assert _parse_string_factory(
        0, "", nre.float_nosign_noexp().split, no_op, fast_float, tuple2
    )("a5+5.034e-1") == ("a", 5.0, "+", 5.034, "e-", 1.0)


@given(
    lists(
        elements=floats(allow_nan=False) | text().filter(whitespace_check) | integers(),
        min_size=1,
        max_size=10,
    )
)
def test_parse_string_factory_only_parses_float_with_nosign_noexp_float(x):
    s = "".join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_factory(
        0, "", nre.float_nosign_noexp().split, no_op, fast_float, tuple2
    )(s) == float_splitter(s, False, False, "")


def test_parse_string_factory_only_parses_float_with_exponent_with_nosign_exp_float_example():
    assert _parse_string_factory(
        0, "", nre.float_nosign_exp().split, no_op, fast_float, tuple2
    )("a5+5.034e-1") == ("a", 5.0, "+", 0.5034)


@given(
    lists(
        elements=floats(allow_nan=False) | text().filter(whitespace_check) | integers(),
        min_size=1,
        max_size=10,
    )
)
def test_parse_string_factory_only_parses_float_with_exponent_with_nosign_exp_float(x):
    s = "".join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_factory(
        0, "", nre.float_nosign_exp().split, no_op, fast_float, tuple2
    )(s) == float_splitter(s, False, True, "")


def test_parse_string_factory_only_parses_float_with_sign_with_sign_noexp_float_example():
    assert _parse_string_factory(
        0, "", nre.float_sign_noexp().split, no_op, fast_float, tuple2
    )("a5+5.034e-1") == ("a", 5.0, "", 5.034, "e", -1.0)


@given(
    lists(
        elements=floats(allow_nan=False) | text().filter(whitespace_check) | integers(),
        min_size=1,
        max_size=10,
    )
)
def test_parse_string_factory_only_parses_float_with_sign_with_sign_noexp_float(x):
    s = "".join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_factory(
        0, "", nre.float_sign_noexp().split, no_op, fast_float, tuple2
    )(s) == float_splitter(s, True, False, "")


def test_parse_string_factory_parses_float_with_sign_exp_float_example():
    assert _parse_string_factory(
        0, "", nre.float_sign_exp().split, no_op, fast_float, tuple2
    )("a5+5.034e-1") == ("a", 5.0, "", 0.5034)
    assert _parse_string_factory(
        0, "", nre.float_sign_exp().split, no_op, fast_float, tuple2
    )("6a5+5.034e-1") == ("", 6.0, "a", 5.0, "", 0.5034)


@given(
    lists(
        elements=floats(allow_nan=False) | text().filter(whitespace_check) | integers(),
        min_size=1,
        max_size=10,
    )
)
def test_parse_string_factory_parses_float_with_sign_exp_float(x):
    s = "".join(repr(y) if type(y) in (float, long, int) else y for y in x)
    assert _parse_string_factory(
        0, "", nre.float_sign_exp().split, no_op, fast_float, tuple2
    )(s) == float_splitter(s, True, True, "")


def test_parse_string_factory_selects_pre_function_value_if_not_dumb():
    def tuple2(x, orig):
        """Make the input a tuple."""
        return (orig[0], tuple(x))

    assert _parse_string_factory(
        0, "", nre.int_nosign().split, py23_str.upper, fast_float, tuple2
    )("a5+5.034e-1") == ("A", ("A", 5, "+", 5, ".", 34, "E-", 1))
    assert _parse_string_factory(
        ns_DUMB, "", nre.int_nosign().split, py23_str.upper, fast_float, tuple2
    )("a5+5.034e-1") == ("A", ("A", 5, "+", 5, ".", 34, "E-", 1))
    assert _parse_string_factory(
        ns.LOCALE, "", nre.int_nosign().split, py23_str.upper, fast_float, tuple2
    )("a5+5.034e-1") == ("A", ("A", 5, "+", 5, ".", 34, "E-", 1))
    assert _parse_string_factory(
        ns.LOCALE | ns_DUMB,
        "",
        nre.int_nosign().split,
        py23_str.upper,
        fast_float,
        tuple2,
    )("a5+5.034e-1") == ("a", ("A", 5, "+", 5, ".", 34, "E-", 1))


def test_parse_path_function_parses_string_as_path_then_as_string():
    splt = _parse_string_factory(
        0, "", nre.float_sign_exp().split, no_op, fast_float, tuple2
    )
    assert _parse_path_factory(splt)("/p/Folder (10)/file34.5nm (2).tar.gz") == (
        ("/",),
        ("p",),
        ("Folder (", 10.0, ")"),
        ("file", 34.5, "nm (", 2.0, ")"),
        (".tar",),
        (".gz",),
    )
    assert _parse_path_factory(splt)("../Folder (10)/file (2).tar.gz") == (
        ("..",),
        ("Folder (", 10.0, ")"),
        ("file (", 2.0, ")"),
        (".tar",),
        (".gz",),
    )
    assert _parse_path_factory(splt)("Folder (10)/file.f34.5nm (2).tar.gz") == (
        ("Folder (", 10.0, ")"),
        ("file.f", 34.5, "nm (", 2.0, ")"),
        (".tar",),
        (".gz",),
    )
