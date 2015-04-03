# -*- coding: utf-8 -*-
"""These test the utils.py functions."""

import locale
from operator import itemgetter
from pytest import raises
from natsort.ns_enum import ns
from natsort.utils import _number_extracter, _py3_safe, _natsort_key, _args_to_enum
from natsort.utils import _float_sign_exp_re, _float_nosign_exp_re, _float_sign_noexp_re
from natsort.utils import _float_nosign_noexp_re, _int_nosign_re, _int_sign_re
from natsort.locale_help import use_pyicu, null_string

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


def test_args_to_enum_converts_signed_exp_float_to_ns_F():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(float, True, True, False, False) == ns.F


def test_args_to_enum_converts_signed_noexp_float_to_ns_FN():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(float, True, False, False, False) == ns.F | ns.N


def test_args_to_enum_converts_unsigned_exp_float_to_ns_FU():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(float, False, True, False, False) == ns.F | ns.U


def test_args_to_enum_converts_unsigned_unexp_float_to_ns_FNU():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(float, False, False, False, False) == ns.F | ns.U | ns.N


def test_args_to_enum_converts_signed_exp_float_and_path_and_py3safe_to_ns_FPT():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(float, True, True, True, True) == ns.F | ns.P | ns.T


def test_args_to_enum_converts_singed_int_and_path_to_ns_IP():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(int, True, True, True, False) == ns.I | ns.P


def test_args_to_enum_converts_unsigned_int_and_py3safe_to_ns_IUT():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(int, False, True, False, True) == ns.I | ns.U | ns.T


def test_args_to_enum_converts_None_to_ns_IU():
    # number_type, signed, exp, as_path, py3_safe
    assert _args_to_enum(None, True, True, False, False) == ns.I | ns.U

# fttt = (fast_float, True, True, True)
# fttf = (fast_float, True, True, False)
ftft = (fast_float, True, False, True)
ftff = (fast_float, True, False, False)
# fftt = (fast_float, False, True, True)
ffft = (fast_float, False, False, True)
# fftf = (fast_float, False, True, False)
ffff = (fast_float, False, False, False)
ittt = (fast_int, True, True, True)
ittf = (fast_int, True, True, False)
itft = (fast_int, True, False, True)
itff = (fast_int, True, False, False)
# iftt = (fast_int, False, True, True)
ifft = (fast_int, False, False, True)
# iftf = (fast_int, False, True, False)
ifff = (fast_int, False, False, False)


def test_number_extracter_raises_TypeError_if_given_a_number():
    with raises(TypeError):
        assert _number_extracter(50.0, _float_sign_exp_re, *ffff)


def test_number_extracter_includes_plus_sign_and_exponent_in_float_definition_for_signed_exp_floats():
    assert _number_extracter('a5+5.034e-1', _float_sign_exp_re, *ffff) == ['a', 5.0, 0.5034]


def test_number_extracter_excludes_plus_sign_in_float_definition_but_includes_exponent_for_unsigned_exp_floats():
    assert _number_extracter('a5+5.034e-1', _float_nosign_exp_re, *ffff) == ['a', 5.0, '+', 0.5034]


def test_number_extracter_includes_plus_and_minus_sign_in_float_definition_but_excludes_exponent_for_signed_noexp_floats():
    assert _number_extracter('a5+5.034e-1', _float_sign_noexp_re, *ffff) == ['a', 5.0, 5.034, 'e', -1.0]


def test_number_extracter_excludes_plus_sign_and_exponent_in_float_definition_for_unsigned_noexp_floats():
    assert _number_extracter('a5+5.034e-1', _float_nosign_noexp_re, *ffff) == ['a', 5.0, '+', 5.034, 'e-', 1.0]


def test_number_extracter_excludes_plus_and_minus_sign_in_int_definition_for_unsigned_ints():
    assert _number_extracter('a5+5.034e-1', _int_nosign_re, *ifff) == ['a', 5, '+', 5, '.', 34, 'e-', 1]


def test_number_extracter_includes_plus_and_minus_sign_in_int_definition_for_signed_ints():
    assert _number_extracter('a5+5.034e-1', _int_sign_re, *ifff) == ['a', 5, 5, '.', 34, 'e', -1]


def test_number_extracter_inserts_empty_string_between_floats_for_py3safe_option():
    assert _number_extracter('a5+5.034e-1', _float_sign_exp_re, *ftff) == ['a', 5.0, '', 0.5034]


def test_number_extracter_inserts_empty_string_between_ints_for_py3safe_option():
    assert _number_extracter('a5+5.034e-1', _int_sign_re, *itff) == ['a', 5, '', 5, '.', 34, 'e', -1]


def test_number_extracter_inserts_no_empty_string_py3safe_option_because_no_numbers_are_adjascent():
    assert _number_extracter('a5+5.034e-1', _float_nosign_exp_re, *ftff) == ['a', 5.0, '+', 0.5034]


def test_number_extracter_adds_leading_empty_string_if_input_begins_with_a_number():
    assert _number_extracter('6a5+5.034e-1', _float_sign_exp_re, *ffff) == ['', 6.0, 'a', 5.0, 0.5034]


def test_number_extracter_adds_leading_empty_string_if_input_begins_with_a_number_and_empty_string_between_numbers_for_py3safe():
    assert _number_extracter('6a5+5.034e-1', _float_sign_exp_re, *ftff) == ['', 6.0, 'a', 5.0, '', 0.5034]


def test_number_extracter_doubles_letters_with_lowercase_version_with_groupletters_for_float():
    assert _number_extracter('A5+5.034E-1', _float_sign_exp_re, *ffft) == ['aA', 5.0, 0.5034]


def test_number_extracter_doubles_letters_with_lowercase_version_with_groupletters_for_int():
    assert _number_extracter('A5+5.034E-1', _int_nosign_re, *ifft) == ['aA', 5, '++', 5, '..', 34, 'eE--', 1]


def test_number_extracter_extracts_numbers_and_strxfrms_strings_with_use_locale():
    locale.setlocale(locale.LC_NUMERIC, str('en_US.UTF-8'))
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert _number_extracter('A5+5.034E-1', _int_nosign_re, *ittf) == [strxfrm('A'), 5, strxfrm('+'), 5, strxfrm('.'), 34, strxfrm('E-'), 1]
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_number_extracter_extracts_numbers_and_strxfrms_letter_doubled_strings_with_use_locale_and_groupletters():
    locale.setlocale(locale.LC_NUMERIC, str('en_US.UTF-8'))
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert _number_extracter('A5+5.034E-1', _int_nosign_re, *ittt) == [strxfrm('aA'), 5, strxfrm('++'), 5, strxfrm('..'), 34, strxfrm('eE--'), 1]
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_py3_safe_does_nothing_if_no_numbers():
    assert _py3_safe(['a', 'b', 'c'], False) == ['a', 'b', 'c']
    assert _py3_safe(['a'], False) == ['a']


def test_py3_safe_does_nothing_if_only_one_number():
    assert _py3_safe(['a', 5], False) == ['a', 5]


def test_py3_safe_inserts_empty_string_between_two_numbers():
    assert _py3_safe([5, 9], False) == [5, '', 9]


def test_py3_safe_with_use_locale_inserts_null_string_between_two_numbers():
    assert _py3_safe([5, 9], True) == [5, null_string, 9]


def test__natsort_key_with_float_splits_input_into_string_and_signed_float_with_exponent():
    assert ns.F == ns.FLOAT
    assert _natsort_key('a-5.034e2', None, ns.F) == ('a', -503.4)


def test__natsort_key_with_float_and_noexp_splits_input_into_string_and_signed_float_without_exponent():
    assert _natsort_key('a-5.034e2', None, ns.FLOAT | ns.NOEXP) == ('a', -5.034, 'e', 2.0)
    # Default is to split on floats.
    assert _natsort_key('a-5.034e2', None, ns.NOEXP) == ('a', -5.034, 'e', 2.0)


def test__natsort_key_with_float_and_unsigned_splits_input_into_string_and_unsigned_float():
    assert _natsort_key('a-5.034e2', None, ns.UNSIGNED) == ('a-', 503.4)


def test__natsort_key_with_float_and_unsigned_and_noexp_splits_input_into_string_and_unsigned_float_without_exponent():
    assert _natsort_key('a-5.034e2', None, ns.UNSIGNED | ns.NOEXP) == ('a-', 5.034, 'e', 2.0)


def test__natsort_key_with_int_splits_input_into_string_and_signed_int():
    assert _natsort_key('a-5.034e2', None, ns.INT) == ('a', -5, '.', 34, 'e', 2)
    # NOEXP is ignored for integers
    assert _natsort_key('a-5.034e2', None, ns.INT | ns.NOEXP) == ('a', -5, '.', 34, 'e', 2)


def test__natsort_key_with_int_splits_and_unsigned_input_into_string_and_unsigned_int():
    assert _natsort_key('a-5.034e2', None, ns.INT | ns.UNSIGNED) == ('a-', 5, '.', 34, 'e', 2)


def test__natsort_key_with_version_or_digit_matches_usigned_int():
    assert _natsort_key('a-5.034e2', None, ns.VERSION) == _natsort_key('a-5.034e2', None, ns.INT | ns.UNSIGNED)
    assert _natsort_key('a-5.034e2', None, ns.DIGIT) == _natsort_key('a-5.034e2', None, ns.VERSION)


def test__natsort_key_with_key_applies_key_function_before_splitting():
    assert _natsort_key('a-5.034e2', lambda x: x.upper(), ns.F) == ('A', -503.4)


def test__natsort_key_with_tuple_input_returns_nested_tuples():
    # Iterables are parsed recursively so you can sort lists of lists.
    assert _natsort_key(('a1', 'a-5.034e2'), None, ns.V) == (('a', 1), ('a-', 5, '.', 34, 'e', 2))


def test__natsort_key_with_tuple_input_but_itemgetter_key_returns_split_second_element():
    # A key is applied before recursion, but not in the recursive calls.
    assert _natsort_key(('a1', 'a-5.034e2'), itemgetter(1), ns.F) == ('a', -503.4)


def test__natsort_key_with_input_containing_leading_numbers_returns_leading_empty_strings():
    # Strings that lead with a number get an empty string at the front of the tuple.
    # This is designed to get around the "unorderable types" issue.
    assert _natsort_key(('15a', '6'), None, ns.F) == (('', 15.0, 'a'), ('', 6.0))


def test__natsort_key_with_numeric_input_returns_number_with_leading_empty_string():
    assert _natsort_key(10, None, ns.F) == ('', 10)


def test__natsort_key_with_absolute_path_intput_and_PATH_returns_nested_tuple_where_each_element_is_path_component_with_leading_root_and_split_extensions():
    # Turn on PATH to split a file path into components
    assert _natsort_key('/p/Folder (10)/file34.5nm (2).tar.gz', None, ns.PATH) == (('/',), ('p', ), ('Folder (', 10.0, ')',), ('file', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_relative_path_intput_and_PATH_returns_nested_tuple_where_each_element_is_path_component_with_leading_relative_parent_and_split_extensions():
    assert _natsort_key('../Folder (10)/file (2).tar.gz', None, ns.PATH) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_relative_path_intput_and_PATH_returns_nested_tuple_where_each_element_is_path_component_and_split_extensions():
    assert _natsort_key('Folder (10)/file.f34.5nm (2).tar.gz', None, ns.PATH) == (('Folder (', 10.0, ')',), ('file.f', 34.5, 'nm (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_pathlib_intput_and_PATH_returns_nested_tuples():
    # Converts pathlib PurePath (and subclass) objects to string before sorting
    if has_pathlib:
        assert _natsort_key(pathlib.Path('../Folder (10)/file (2).tar.gz'), None, ns.PATH) == (('..', ), ('Folder (', 10.0, ')',), ('file (', 2.0, ')'), ('.tar',), ('.gz',))


def test__natsort_key_with_numeric_input_and_PATH_returns_number_in_nested_tuple():
    # It gracefully handles as_path for numeric input by putting an extra tuple around it
    # so it will sort against the other as_path results.
    assert _natsort_key(10, None, ns.PATH) == (('', 10),)


def test__natsort_key_with_tuple_of_paths_and_PATH_returns_triply_nested_tuple():
    # PATH also handles recursion well.
    assert _natsort_key(('/Folder', '/Folder (1)'), None, ns.PATH) == ((('/',), ('Folder',)), (('/',), ('Folder (', 1.0, ')')))


def test__natsort_key_with_TYPESAFE_inserts_spaces_between_numbers():
    # Turn on TYPESAFE to put a '' between adjacent numbers
    assert _natsort_key('43h7+3', None, ns.TYPESAFE) == ('', 43.0, 'h', 7.0, '', 3.0)


def test__natsort_key_with_invalid_alg_input_raises_ValueError():
    # Invalid arguments give the correct response
    with raises(ValueError) as err:
        _natsort_key('a', None, '1')
    assert str(err.value) == "_natsort_key: 'alg' argument must be from the enum 'ns', got 1"


def test__natsort_key_without_string_modifiers_leaves_text_as_is():
    # Changing the sort order of strings
    assert _natsort_key('Apple56', None, ns.F) == ('Apple', 56.0)


def test__natsort_key_with_IGNORECASE_lowercases_text():
    assert _natsort_key('Apple56', None, ns.IGNORECASE) == ('apple', 56.0)


def test__natsort_key_with_LOWERCASEFIRST_inverts_text_case():
    assert _natsort_key('Apple56', None, ns.LOWERCASEFIRST) == ('aPPLE', 56.0)


def test__natsort_key_with_GROUPLETTERS_doubles_text_with_lowercase_letter_first():
    assert _natsort_key('Apple56', None, ns.GROUPLETTERS) == ('aAppppllee', 56.0)


def test__natsort_key_with_GROUPLETTERS_and_LOWERCASEFIRST_inverts_text_first_then_doubles_letters_with_lowercase_letter_first():
    assert _natsort_key('Apple56', None, ns.G | ns.LF) == ('aapPpPlLeE', 56.0)


def test__natsort_key_with_LOCALE_transforms_floats_according_to_the_current_locale_and_strxfrms_strings():
    # Locale aware sorting
    locale.setlocale(locale.LC_NUMERIC, str('en_US.UTF-8'))
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert _natsort_key('Apple56.5', None, ns.LOCALE) == (strxfrm('Apple'), 56.5)
    assert _natsort_key('Apple56,5', None, ns.LOCALE) == (strxfrm('Apple'), 56.0, strxfrm(','), 5.0)

    locale.setlocale(locale.LC_NUMERIC, str('de_DE.UTF-8'))
    if use_pyicu:
        strxfrm = get_pyicu_transform(getlocale())
    assert _natsort_key('Apple56.5', None, ns.LOCALE) == (strxfrm('Apple'), 56.5)
    assert _natsort_key('Apple56,5', None, ns.LOCALE) == (strxfrm('Apple'), 56.5)
    locale.setlocale(locale.LC_NUMERIC, str(''))
