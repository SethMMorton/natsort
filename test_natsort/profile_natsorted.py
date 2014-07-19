# -*- coding: utf-8 -*-
"""\
This file contains functions to profile natsorted with different
inputs and different settings.
"""
from __future__ import print_function
import cProfile
import random
import sys

sys.path.insert(0, '.')
from natsort import natsorted, index_natsorted
from natsort.py23compat import py23_range


# Sample lists to sort
nums = random.sample(py23_range(10000), 1000)
nstr = list(map(str, random.sample(py23_range(10000), 1000)))
astr = ['a'+x+'num' for x in map(str, random.sample(py23_range(10000), 1000))]
tstr = [['a'+x, 'a-'+x]
        for x in map(str, random.sample(py23_range(10000), 1000))]
cstr = ['a'+x+'-'+x for x in map(str, random.sample(py23_range(10000), 1000))]


def prof_nums(a):
    print('*** Basic Call, Numbers ***')
    for _ in py23_range(1000):
        natsorted(a)
cProfile.run('prof_nums(nums)', sort='time')


def prof_num_str(a):
    print('*** Basic Call, Numbers as Strings ***')
    for _ in py23_range(1000):
        natsorted(a)
cProfile.run('prof_num_str(nstr)', sort='time')


def prof_str(a):
    print('*** Basic Call, Strings ***')
    for _ in py23_range(1000):
        natsorted(a)
cProfile.run('prof_str(astr)', sort='time')


def prof_str_index(a):
    print('*** Basic Index Call ***')
    for _ in py23_range(1000):
        index_natsorted(a)
cProfile.run('prof_str_index(astr)', sort='time')


def prof_nested(a):
    print('*** Basic Call, Nested Strings ***')
    for _ in py23_range(1000):
        natsorted(a)
cProfile.run('prof_nested(tstr)', sort='time')


def prof_str_noexp(a):
    print('*** No-Exp Call ***')
    for _ in py23_range(1000):
        natsorted(a, exp=False)
cProfile.run('prof_str_noexp(astr)', sort='time')


def prof_str_unsigned(a):
    print('*** Unsigned Call ***')
    for _ in py23_range(1000):
        natsorted(a, signed=False)
cProfile.run('prof_str_unsigned(astr)', sort='time')


def prof_str_unsigned_noexp(a):
    print('*** Unsigned No-Exp Call ***')
    for _ in py23_range(1000):
        natsorted(a, signed=False, exp=False)
cProfile.run('prof_str_unsigned_noexp(astr)', sort='time')


def prof_str_asint(a):
    print('*** Int Call ***')
    for _ in py23_range(1000):
        natsorted(a, number_type=int)
cProfile.run('prof_str_asint(astr)', sort='time')


def prof_str_asint_unsigned(a):
    print('*** Unsigned Int (Versions) Call ***')
    for _ in py23_range(1000):
        natsorted(a, number_type=int, signed=False)
cProfile.run('prof_str_asint_unsigned(astr)', sort='time')


def prof_str_key(a):
    print('*** Basic Call With Key ***')
    for _ in py23_range(1000):
        natsorted(a, key=lambda x: x.upper())
cProfile.run('prof_str_key(astr)', sort='time')


def prof_str_index_key(a):
    print('*** Basic Index Call With Key ***')
    for _ in py23_range(1000):
        index_natsorted(a, key=lambda x: x.upper())
cProfile.run('prof_str_index_key(astr)', sort='time')


def prof_str_unorderable(a):
    print('*** Basic Index Call, "Unorderable" ***')
    for _ in py23_range(1000):
        natsorted(a)
cProfile.run('prof_str_unorderable(cstr)', sort='time')
