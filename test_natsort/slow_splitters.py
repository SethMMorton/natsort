# -*- coding: utf-8 -*-
"""Alternate versions of the splitting functions for testing."""
from __future__ import unicode_literals

import unicodedata
import collections
import itertools
from natsort.compat.py23 import PY_VERSION, py23_zip, py23_map

if PY_VERSION >= 3.0:
    long = int


def int_splitter(iterable, signed, safe, sep):
    """Alternate (slow) method to split a string into numbers."""
    split_by_digits = itertools.groupby(iterable, lambda a: a.isdigit())
    split_by_digits = refine_split_grouping(split_by_digits)
    split = int_splitter_iter(split_by_digits, signed)
    if safe:
        split = sep_inserter(split, sep)
    return list(add_leading_space_if_first_is_num(split, sep))


def refine_split_grouping(iterable):
    """Combines lists into strings, and separates unicode numbers from ASCII"""
    SplitElement = collections.namedtuple('SplitElement',
                                          ['isnum', 'val', 'isuni'])
    for isnum, values in iterable:
        values = list(values)
        # Further refine numbers into unicode and ASCII numeric characters.
        if isnum:
            num_grouped = group_unicode_and_ascii_numbers(values)
            for isuni, num_values in num_grouped:
                # If unicode, return one character at a time.
                if isuni:
                    for u in num_values:
                        yield SplitElement(True, u, True)
                # If ASCII, combine into a single multicharacter number.
                else:
                    val = ''.join(num_values)
                    yield SplitElement(True, val, False)

        else:
            # If non-numeric, combine into a single string.
            val = ''.join(values)
            yield SplitElement(False, val, False)


def group_unicode_and_ascii_numbers(iterable, ascii_digits=set('0123456789')):
    """
    Use groupby to group ASCII and unicode numeric characters.
    Assumes all input is already all numeric characters.
    """
    return itertools.groupby(iterable, lambda a: a not in ascii_digits)


def int_splitter_iter(iterable, signed):
    """Split the input into unsigned integers and other."""
    for isnum, val, isuni in iterable:
        if isnum and isuni:
            yield unicodedata.digit(val)
        elif isnum:
            yield int(val)
        elif signed:
            for x in try_to_read_signed_integer(iterable, val):
                yield x
        else:
            yield val


def try_to_read_signed_integer(iterable, val):
    """
    If the given string ends with +/-, attempt to return a signed int.
    Otherwise, return the string as-is.
    """
    if val.endswith('+') or val.endswith('-'):
        next_element = next(iterable, None)

        # Last element, return as-is.
        if next_element is None:
            yield val

        # We know the next value in the sequence must be "isnum == True".
        # We just need to handle unicode or not.
        else:
            _, next_val, next_isuni = next_element

            # If unicode, don't apply sign and just return the val as-is
            # and convert the unicode character.
            if next_isuni:
                yield val
                yield unicodedata.digit(next_val)

            # If the val is *only* the sign, return only the number.
            elif val in ('-', '+'):
                yield int(val + next_val)

            # Otherwise, remove the sign from the val and apply it to the number,
            # returning both.
            else: 
                yield val[:-1]
                yield int(val[-1] + next_val)

    else:
        yield val


def add_leading_space_if_first_is_num(iterable, sep):
    """Check if the first element is a number, and prepend with space if so."""
    z, peek = itertools.tee(iterable)
    if type(next(peek, None)) in (int, long, float):
        z = itertools.chain([sep], z)
    del peek
    return z


def sep_inserter(iterable, sep, t=set((int, long, float))):
    """Simulates the py3_safe function."""
    pairs = pairwise(iterable)

    # Prime loop by handling first pair specially.
    first, second = next(pairs)
    if second is None:  # Only one element
        yield first
    elif type(first) in t and type(second) in t:
        yield first
        yield sep
        yield second
    else:
        yield first
        yield second

    # Handle all remaining pairs in loop.
    for first, second in pairs:
        if type(first) in t and type(second) in t:
            yield sep
        yield second


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2,s3), ..."
    split1, split2 = itertools.tee(iterable)
    a, b = itertools.tee(split1)
    test1, test2 = itertools.tee(split2)
    next(b, None)
    if next(test1, None) is None:
        ret = py23_zip(a, b)  # Returns empty list
    elif next(test2, None) is not None and next(test2, None) is None:
        ret = py23_zip(a, [None])  # Return at least one value
    else:
        ret = py23_zip(a, b)
    del test1, test2, split2
    return ret


def float_splitter(x, signed, exp, safe, sep):
    """Alternate (slow) method to split a string into numbers."""
    # Hacked together and not maintainable.
    if not x:
        return []
    all_digits = set('0123456789')
    full_list, strings, nums = [], [], []
    input_len = len(x)
    for i, char in enumerate(x):
        # If this character is a sign and the next is a number,
        # start a new number.
        if (i+1 < input_len and
                (signed or (nums and i > 1 and exp and x[i-1] in 'eE' and
                            x[i-2] in all_digits)) and
                (char in '-+') and (x[i+1] in all_digits | set('.'))):
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
            if nums and ('.' in nums or 'e' in nums or 'E' in nums):
                full_list.append(float(''.join(nums)))
                nums = []
            nums.append(char)
            if strings:
                full_list.append(''.join(strings))
            strings = []
        # If this is an exponent, add to the number list.
        elif (i > 0 and i + 2 < input_len and exp and char in 'eE' and
                x[i-1] in all_digits and x[i+1] in set('+-') and
                x[i+2] in all_digits):
            if 'e' in nums or 'E' in nums:
                strings = [char]
                full_list.append(float(''.join(nums)))
                nums = []
            else:
                nums.append(char)
        elif (i > 0 and i + 1 < input_len and exp and char in 'eE' and
                x[i-1] in all_digits and x[i+1] in all_digits):
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
    full_list = [float(y)
                 if type(y) != float and y.lower().strip(' \t\n')
                 in fstrings else y
                 for y in full_list]
    if safe:
        full_list = list(sep_inserter(full_list, sep))
    if type(full_list[0]) == float:
        return [sep] + full_list
    else:
        return full_list
