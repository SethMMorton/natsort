# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import unicode_literals, print_function
import pytest
import locale
from natsort.compat.py23 import PY_VERSION
from operator import itemgetter
from pytest import raises
from natsort import (
    natsorted,
    ns,
)
from compat.locale import (
    load_locale,
    has_locale_de_DE,
)


def test_natsorted_returns_strings_with_numbers_in_ascending_order():
    a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
    assert natsorted(a) == ['a1', 'a2', 'a4', 'a5', 'a6', 'a9', 'a10']


def test_natsorted_returns_list_of_numbers_sorted_as_signed_floats_with_exponents():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.REAL) == ['a-50', 'a50', 'a50.300', 'a50.31', 'a5.034e1', 'a50.4', 'a51.']


def test_natsorted_returns_list_of_numbers_sorted_as_unsigned_floats_without_exponents_with_NOEXP_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.N | ns.F | ns.U) == ['a5.034e1', 'a50', 'a50.300', 'a50.31', 'a50.4', 'a51.', 'a-50']
    # UNSIGNED is default
    assert natsorted(a, alg=ns.NOEXP | ns.FLOAT) == ['a5.034e1', 'a50', 'a50.300', 'a50.31', 'a50.4', 'a51.', 'a-50']


def test_natsorted_returns_list_of_numbers_sorted_as_unsigned_ints_with_INT_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.INT) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']
    # INT is default
    assert natsorted(a) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']


def test_natsorted_returns_list_of_numbers_sorted_as_unsigned_ints_with_DIGIT_and_VERSION_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.DIGIT) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']
    assert natsorted(a, alg=ns.VERSION) == ['a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.', 'a-50']


def test_natsorted_returns_list_of_numbers_sorted_as_signed_ints_with_SIGNED_option():
    a = ['a50', 'a51.', 'a50.31', 'a-50', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, alg=ns.SIGNED) == ['a-50', 'a5.034e1', 'a50', 'a50.4', 'a50.31', 'a50.300', 'a51.']


def test_natsorted_returns_list_of_numbers_sorted_accounting_for_sign_with_SIGNED_option():
    a = ['a-5', 'a7', 'a+2']
    assert natsorted(a, alg=ns.SIGNED) == ['a-5', 'a+2', 'a7']


def test_natsorted_returns_list_of_numbers_sorted_not_accounting_for_sign_without_SIGNED_option():
    a = ['a-5', 'a7', 'a+2']
    assert natsorted(a) == ['a7', 'a+2', 'a-5']


def test_natsorted_returns_sorted_list_of_version_numbers_by_default_or_with_VERSION_option():
    a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    assert natsorted(a) == ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']
    assert natsorted(a, alg=ns.VERSION) == ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']


def test_natsorted_returns_sorted_list_with_mixed_type_input_and_does_not_raise_TypeError_on_Python3():
    # You can mix types with natsorted.  This can get around the new
    # 'unorderable types' issue with Python 3.
    a = [6, 4.5, '7', '2.5', 'a']
    assert natsorted(a) == ['2.5', 4.5, 6, '7', 'a']
    a = [46, '5a5b2', 'af5', '5a5-4']
    assert natsorted(a) == ['5a5-4', '5a5b2', 46, 'af5']


def test_natsorted_with_mixed_input_returns_sorted_results_without_error():
    a = ['0', 'Á', '2', 'Z']
    assert natsorted(a) == ['0', '2', 'Á', 'Z']
    a = ['2', 'ä', 'b', 1.5, 3]
    assert natsorted(a) == [1.5, '2', 3, 'ä', 'b']


def test_natsorted_with_nan_input_returns_sorted_results_with_nan_last_with_NANLAST():
    a = ['25', 5, float('nan'), 1E40]
    # The slice is because NaN != NaN
    assert natsorted(a, alg=ns.NANLAST)[:3] == [5, '25', 1E40, float('nan')][:3]


def test_natsorted_with_nan_input_returns_sorted_results_with_nan_first_without_NANLAST():
    a = ['25', 5, float('nan'), 1E40]
    # The slice is because NaN != NaN
    assert natsorted(a)[1:] == [float('nan'), 5, '25', 1E40][1:]


def test_natsorted_with_mixed_input_raises_TypeError_if_bytes_type_is_involved_on_Python3():
    if PY_VERSION >= 3:
        with raises(TypeError) as e:
            assert natsorted(['ä', b'b'])
        assert 'bytes' in str(e.value)
    else:
        assert True


def test_natsorted_raises_ValueError_for_non_iterable_input():
    with raises(TypeError) as err:
        natsorted(100)
    assert str(err.value) == "'int' object is not iterable"


def test_natsorted_recursivley_applies_key_to_nested_lists_to_return_sorted_nested_list():
    data = [['a1', 'a5'], ['a1', 'a40'], ['a10', 'a1'], ['a2', 'a5']]
    assert natsorted(data) == [['a1', 'a5'], ['a1', 'a40'], ['a2', 'a5'], ['a10', 'a1']]


def test_natsorted_applies_key_to_each_list_element_before_sorting_list():
    b = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
    assert natsorted(b, key=itemgetter(1)) == [('c', 'num2'), ('a', 'num3'), ('b', 'num5')]


def test_natsorted_returns_list_in_reversed_order_with_reverse_option():
    a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    assert natsorted(a, reverse=True) == natsorted(a)[::-1]


def test_natsorted_sorts_OS_generated_paths_incorrectly_without_PATH_option():
    a = ['/p/Folder (10)/file.tar.gz',
         '/p/Folder/file.tar.gz',
         '/p/Folder (1)/file (1).tar.gz',
         '/p/Folder (1)/file.tar.gz']
    assert natsorted(a) == ['/p/Folder (1)/file (1).tar.gz',
                            '/p/Folder (1)/file.tar.gz',
                            '/p/Folder (10)/file.tar.gz',
                            '/p/Folder/file.tar.gz']


def test_natsorted_sorts_OS_generated_paths_correctly_with_PATH_option():
    a = ['/p/Folder (10)/file.tar.gz',
         '/p/Folder/file.tar.gz',
         '/p/Folder (1)/file (1).tar.gz',
         '/p/Folder (1)/file.tar.gz']
    assert natsorted(a, alg=ns.PATH) == ['/p/Folder/file.tar.gz',
                                         '/p/Folder (1)/file.tar.gz',
                                         '/p/Folder (1)/file (1).tar.gz',
                                         '/p/Folder (10)/file.tar.gz']


def test_natsorted_can_handle_sorting_paths_and_numbers_with_PATH():
    # You can sort paths and numbers, not that you'd want to
    a = ['/Folder (9)/file.exe', 43]
    assert natsorted(a, alg=ns.PATH) == [43, '/Folder (9)/file.exe']


def test_natsorted_returns_results_in_ASCII_order_with_no_case_options():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a) == ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']


def test_natsorted_returns_results_sorted_by_lowercase_ASCII_order_with_IGNORECASE():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.IGNORECASE) == ['Apple', 'apple', 'Banana', 'banana', 'corn', 'Corn']


def test_natsorted_returns_results_in_ASCII_order_but_with_lowercase_letters_first_with_LOWERCASEFIRST():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.LOWERCASEFIRST) == ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']


def test_natsorted_returns_results_with_uppercase_and_lowercase_letters_grouped_together_with_GROUPLETTERS():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.GROUPLETTERS) == ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']


def test_natsorted_returns_results_in_natural_order_with_GROUPLETTERS_and_LOWERCASEFIRST():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    assert natsorted(a, alg=ns.G | ns.LF) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']


def test_natsorted_places_uppercase_letters_before_lowercase_letters_for_nested_input():
    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b) == [('A5', 'a6'), ('a3', 'a1')]


def test_natsorted_with_LOWERCASEFIRST_places_lowercase_letters_before_uppercase_letters_for_nested_input():
    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b, alg=ns.LOWERCASEFIRST) == [('a3', 'a1'), ('A5', 'a6')]


def test_natsorted_with_IGNORECASE_sorts_without_regard_to_case_for_nested_input():
    b = [('A5', 'a6'), ('a3', 'a1')]
    assert natsorted(b, alg=ns.IGNORECASE) == [('a3', 'a1'), ('A5', 'a6')]


def test_natsorted_with_LOCALE_returns_results_sorted_by_lowercase_first_and_grouped_letters():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE) == ['apple', 'Apple', 'banana', 'Banana', 'corn', 'Corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_CAPITALFIRST_returns_results_sorted_by_capital_first_and_ungrouped():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE | ns.CAPITALFIRST) == ['Apple', 'Banana', 'Corn', 'apple', 'banana', 'corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_LOWERCASEFIRST_returns_results_sorted_by_uppercase_first_and_grouped_letters():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE | ns.LOWERCASEFIRST) == ['Apple', 'apple', 'Banana', 'banana', 'Corn', 'corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_CAPITALFIRST_and_LOWERCASE_returns_results_sorted_by_capital_last_and_ungrouped():
    a = ['Apple', 'corn', 'Corn', 'Banana', 'apple', 'banana']
    load_locale('en_US')
    assert natsorted(a, alg=ns.LOCALE | ns.CAPITALFIRST | ns.LOWERCASEFIRST) == ['apple', 'banana', 'corn', 'Apple', 'Banana', 'Corn']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_en_setting_returns_results_sorted_by_en_language():
    load_locale('en_US')
    a = ['c', 'a5,467.86', 'ä', 'b', 'a5367.86', 'a5,6', 'a5,50']
    assert natsorted(a, alg=ns.LOCALE | ns.F) == ['a5,6', 'a5,50', 'a5367.86', 'a5,467.86', 'ä', 'b', 'c']
    locale.setlocale(locale.LC_ALL, str(''))


@pytest.mark.skipif(not has_locale_de_DE, reason='requires de_DE locale and working locale')
def test_natsorted_with_LOCALE_and_de_setting_returns_results_sorted_by_de_language():
    load_locale('de_DE')
    a = ['c', 'a5.467,86', 'ä', 'b', 'a5367.86', 'a5,6', 'a5,50']
    assert natsorted(a, alg=ns.LOCALE | ns.F) == ['a5,50', 'a5,6', 'a5367.86', 'a5.467,86', 'ä', 'b', 'c']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_mixed_input_returns_sorted_results_without_error():
    load_locale('en_US')
    a = ['0', 'Á', '2', 'Z']
    assert natsorted(a, alg=ns.LOCALE) == ['0', '2', 'Á', 'Z']
    a = ['2', 'ä', 'b', 1.5, 3]
    assert natsorted(a, alg=ns.LOCALE) == [1.5, '2', 3, 'ä', 'b']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_LOCALE_and_UNGROUPLETTERS_and_mixed_input_returns_sorted_results_without_error():
    load_locale('en_US')
    a = ['0', 'Á', '2', 'Z']
    assert natsorted(a, alg=ns.LOCALE | ns.UNGROUPLETTERS) == ['0', '2', 'Á', 'Z']
    a = ['2', 'ä', 'b', 1.5, 3]
    assert natsorted(a, alg=ns.LOCALE | ns.UNGROUPLETTERS) == [1.5, '2', 3, 'ä', 'b']
    locale.setlocale(locale.LC_ALL, str(''))


def test_natsorted_with_PATH_and_LOCALE_and_UNGROUPLETTERS_and_mixed_input_returns_sorted_results_without_error():
    load_locale('en_US')
    a = ['0', 'Á', '2', 'Z']
    assert natsorted(a, alg=ns.PATH | ns.LOCALE | ns.UNGROUPLETTERS) == ['0', '2', 'Á', 'Z']
    a = ['2', 'ä', 'b', 1.5, 3]
    assert natsorted(a, alg=ns.PATH | ns.LOCALE | ns.UNGROUPLETTERS) == [1.5, '2', 3, 'ä', 'b']
    locale.setlocale(locale.LC_ALL, str(''))
