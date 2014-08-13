# -*- coding: utf-8 -*-
"""\
Test the fake fastnumbers module.
"""
from natsort.fake_fastnumbers import fast_float, fast_int, isreal


def test_fast_float():
    assert fast_float('45.8') == 45.8
    assert fast_float('-45') == -45.0
    assert fast_float('45.8e-2') == 45.8e-2
    assert fast_float('invalid') == 'invalid'


def test_fast_int():
    assert fast_int('45.8') == '45.8'
    assert fast_int('-45') == -45
    assert fast_int('+45') == 45
    assert fast_int('invalid') == 'invalid'


def test_isreal():
    assert not isreal('45.8')
    assert isreal(-45)
    assert isreal(45.8e-2)
    assert not isreal('invalid')
