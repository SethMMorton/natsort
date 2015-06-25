# -*- coding: utf-8 -*-
"""Alternate versions of the splitting functions for testing."""
from __future__ import unicode_literals

import unicodedata
from natsort.compat.py23 import PY_VERSION

if PY_VERSION >= 3.0:
    long = int


def int_splitter(x, signed, safe, sep):
    """Alternate (slow) method to split a string into numbers."""
    if not x:
        return []
    all_digits = set('0123456789')
    full_list, strings, nums = [], [], []
    input_len = len(x)
    for i, char in enumerate(x):
        # If this character is a sign and the next is a number,
        # start a new number.
        if (i+1 < input_len and signed and
                (char in '-+') and (x[i+1] in all_digits)):
            # Reset any current string or number.
            if strings:
                full_list.append(''.join(strings))
            if nums:
                full_list.append(int(''.join(nums)))
            strings = []
            nums = [char]
        # If this is a number, add to the number list.
        elif char in all_digits:
            nums.append(char)
            # Reset any string.
            if strings:
                full_list.append(''.join(strings))
            strings = []
        # If this is a unicode digit, append directly to the full list.
        elif char.isdigit():
            # Reset any string or number.
            if strings:
                full_list.append(''.join(strings))
            if nums:
                full_list.append(int(''.join(nums)))
            strings = []
            nums = []
            full_list.append(unicodedata.digit(char))
        # Otherwise add to the string.
        else:
            strings.append(char)
            # Reset any number.
            if nums:
                full_list.append(int(''.join(nums)))
            nums = []
    if nums:
        full_list.append(int(''.join(nums)))
    elif strings:
        full_list.append(''.join(strings))
    if safe:
        full_list = sep_inserter(full_list, (int, long), sep)
    if type(full_list[0]) in (int, long):
        return [sep] + full_list
    else:
        return full_list


def float_splitter(x, signed, exp, safe, sep):
    """Alternate (slow) method to split a string into numbers."""
    if not x:
        return []
    all_digits = set('0123456789')
    full_list, strings, nums = [], [], []
    input_len = len(x)
    for i, char in enumerate(x):
        # If this character is a sign and the next is a number,
        # start a new number.
        if (i+1 < input_len and
                (signed or (i > 1 and exp and x[i-1] in 'eE' and
                            x[i-2] in all_digits)) and
                (char in '-+') and (x[i+1] in all_digits)):
            # Reset any current string or number.
            if strings:
                full_list.append(''.join(strings))
            if nums and i > 0 and x[i-1] not in 'eE':
                full_list.append(float(''.join(nums)))
                nums = [char]
            else:
                nums.append(char)
            strings = []
        # If this is a number, add to the number list.
        elif char in all_digits:
            nums.append(char)
            # Reset any string.
            if strings:
                full_list.append(''.join(strings))
            strings = []
        # If this is a decimal, add to the number list.
        elif (i + 1 < input_len and char == '.' and x[i+1] in all_digits):
            if nums and '.' in nums:
                full_list.append(float(''.join(nums)))
                nums = []
            nums.append(char)
            if strings:
                full_list.append(''.join(strings))
            strings = []
        # If this is an exponent, add to the number list.
        elif (i > 0 and i + 1 < input_len and exp and char in 'eE' and
                x[i-1] in all_digits and x[i+1] in all_digits | set('+-')):
            if 'e' in nums or 'E' in nums:
                strings = [char]
                full_list.append(float(''.join(nums)))
                nums = []
            else:
                nums.append(char)
        # If this is a unicode digit, append directly to the full list.
        elif unicodedata.numeric(char, None) is not None:
            # Reset any string or number.
            if strings:
                full_list.append(''.join(strings))
            if nums:
                full_list.append(float(''.join(nums)))
            strings = []
            nums = []
            full_list.append(unicodedata.numeric(char))
        # Otherwise add to the string.
        else:
            strings.append(char)
            # Reset any number.
            if nums:
                full_list.append(float(''.join(nums)))
            nums = []
    if nums:
        full_list.append(float(''.join(nums)))
    elif strings:
        full_list.append(''.join(strings))
    # Fix a float that looks like a string.
    fstrings = ('inf', 'infinity', '-inf', '-infinity',
                '+inf', '+infinity', 'nan')
    full_list = [float(y) if type(y) != float and y.lower() in fstrings else y
                 for y in full_list]
    if safe:
        full_list = sep_inserter(full_list, (float,), sep)
    if type(full_list[0]) == float:
        return [sep] + full_list
    else:
        return full_list


def sep_inserter(x, t, sep):
    # Simulates the py3_safe function.
    ret = [x[0]]
    for i, y in enumerate(x[1:]):
        if type(y) in t and type(x[i]) in t:
            ret.append(sep)
        ret.append(y)
    return ret
