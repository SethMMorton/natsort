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
else:
    from natsort.locale_help import strxfrm


def test_grouper():
    assert grouper('HELLO', fast_float) == 'hHeElLlLoO'
    assert grouper('hello', fast_float) == 'hheelllloo'
    assert grouper('45.8e-2', fast_float) == 45.8e-2


def test_locale_convert():
    locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    if use_pyicu:
        from natsort.locale_help import get_pyicu_transform
        from locale import getlocale
        strxfrm = get_pyicu_transform(getlocale())
    else:
        from natsort.locale_help import strxfrm
    assert locale_convert('45.8', fast_float, False) == 45.8
    assert locale_convert('45,8', fast_float, False) == strxfrm('45,8')
    assert locale_convert('hello', fast_float, False) == strxfrm('hello')
    assert locale_convert('hello', fast_float, True) == strxfrm('hheelllloo')
    assert locale_convert('45,8', fast_float, True) == strxfrm('4455,,88')

    locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')
    if use_pyicu:
        strxfrm = get_pyicu_transform(getlocale())
    assert locale_convert('45.8', fast_float, False) == 45.8
    assert locale_convert('45,8', fast_float, False) == 45.8
    assert locale_convert('hello', fast_float, False) == strxfrm('hello')
    assert locale_convert('hello', fast_float, True) == strxfrm('hheelllloo')

    locale.setlocale(locale.LC_NUMERIC, '')
