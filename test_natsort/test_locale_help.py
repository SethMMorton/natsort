# -*- coding: utf-8 -*-
"""\
Test the locale help module module.
"""
import locale
from natsort.fake_fastnumbers import fast_float
from natsort.locale_help import grouper, locale_convert, use_pyicu

if use_pyicu:
    from natsort.locale_help import get_pyicu_transform
    from locale import getlocale
    strxfrm = get_pyicu_transform(getlocale())
else:
    from natsort.locale_help import strxfrm


def test_grouper_returns_letters_with_lowercase_transform_of_letter():
    assert grouper('HELLO', fast_float) == 'hHeElLlLoO'
    assert grouper('hello', fast_float) == 'hheelllloo'


def test_grouper_returns_float_string_as_float():
    assert grouper('45.8e-2', fast_float) == 45.8e-2


def test_locale_convert_transforms_float_string_to_float():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    assert locale_convert('45.8', fast_float, False) == 45.8
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_transforms_nonfloat_string_to_strxfrm_string():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert locale_convert('45,8', fast_float, False) == strxfrm('45,8')
    assert locale_convert('hello', fast_float, False) == strxfrm('hello')
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_with_groupletters_transforms_nonfloat_string_to_strxfrm_string_with_grouped_letters():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert locale_convert('hello', fast_float, True) == strxfrm('hheelllloo')
    assert locale_convert('45,8', fast_float, True) == strxfrm('4455,,88')
    locale.setlocale(locale.LC_NUMERIC, str(''))


def test_locale_convert_transforms_float_string_to_float_with_de_locale():
    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    assert locale_convert('45.8', fast_float, False) == 45.8
    assert locale_convert('45,8', fast_float, False) == 45.8
    locale.setlocale(locale.LC_NUMERIC, str(''))
