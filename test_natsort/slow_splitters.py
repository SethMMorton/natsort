# -*- coding: utf-8 -*-
"""Alternate versions of the splitting functions for testing."""
from __future__ import unicode_literals

import unicodedata
import collections
import itertools
import functools
from natsort.compat.py23 import PY_VERSION, py23_zip

if PY_VERSION >= 3.0:
    long = int

triple_none = None, None, None
_sentinel = object()
SplitElement = collections.namedtuple('SplitElement',
                                      ['isnum', 'val', 'isuni'])


def int_splitter(iterable, signed, sep):
    """Alternate (slow) method to split a string into numbers."""
    iterable = unicodedata.normalize('NFD', iterable)
    split_by_digits = itertools.groupby(iterable, lambda a: a.isdigit())
    split_by_digits = refine_split_grouping(split_by_digits)
    split = int_splitter_iter(split_by_digits, signed)
    split = sep_inserter(split, sep)
    return tuple(add_leading_space_if_first_is_num(split, sep))


def float_splitter(iterable, signed, exp, sep):
    """Alternate (slow) method to split a string into numbers."""

    def number_tester(x):
        return x.isdigit() or unicodedata.numeric(x, None) is not None

    iterable = unicodedata.normalize('NFD', iterable)
    split_by_digits = itertools.groupby(iterable, number_tester)
    split_by_digits = peekable(refine_split_grouping(split_by_digits))
    split = float_splitter_iter(split_by_digits, signed, exp)
    split = sep_inserter(split, sep)
    return tuple(add_leading_space_if_first_is_num(split, sep))


def refine_split_grouping(iterable):
    """Combines lists into strings, and separates unicode numbers from ASCII"""
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


def group_unicode_and_ascii_numbers(iterable,
                                    ascii_digits=frozenset('0123456789')):
    """
    Use groupby to group ASCII and unicode numeric characters.
    Assumes all input is already all numeric characters.
    """
    return itertools.groupby(iterable, lambda a: a not in ascii_digits)


def int_splitter_iter(iterable, signed):
    """Split the input into integers and strings."""
    for isnum, val, isuni in iterable:
        if isuni:
            yield unicodedata.digit(val)
        elif isnum:
            yield int(val)
        elif signed:
            for x in try_to_read_signed_integer(iterable, val):
                yield int(''.join(x)) if isinstance(x, list) else x
        else:
            yield val


def float_splitter_iter(iterable, signed, exp):
    """Split the input into integers and other."""
    weird_check = ('-inf', '-infinity', '+inf', '+infinity',
                   'inf', 'infinity', 'nan', '-nan', '+nan')
    try_to_read_float_correctly = [
        try_to_read_float,
        try_to_read_float_with_exp,
        functools.partial(try_to_read_signed_float_template,
                          key=try_to_read_float),
        functools.partial(try_to_read_signed_float_template,
                          key=try_to_read_float_with_exp),
    ][signed * 2 + exp * 1]  # Choose the appropriate converter function.
    for isnum, val, isuni in iterable:
        if isuni:
            yield unicodedata.numeric(val)
        else:
            for x in try_to_read_float_correctly(iterable, isnum, val):
                if isinstance(x, list):
                    yield float(''.join(x))
                elif x.lower().strip(' \t\n\r\f\v') in weird_check:
                    yield float(x)
                else:
                    yield x


def try_to_read_signed_integer(iterable, val):
    """
    If the given string ends with +/-, attempt to return a signed int.
    Otherwise, return the string as-is.
    """
    if val.endswith(('+', '-')):
        next_element = next(iterable, None)

        # Last element, return as-is.
        if next_element is None:
            yield val
            return

        # We know the next value in the sequence must be "isnum == True".
        # We just need to handle unicode or not.
        _, next_val, next_isuni = next_element

        # If unicode, don't apply sign and just return the val as-is
        # and convert the unicode character.
        if next_isuni:
            yield val
            yield unicodedata.digit(next_val)

        # If the val is *only* the sign, return only the number.
        elif val in ('-', '+'):
            yield [val, next_val]

        # Otherwise, remove the sign from the val and apply it to the number,
        # returning both.
        else:
            yield val[:-1]
            yield [val[-1], next_val]

    else:
        yield val


def try_to_read_float(iterable, isnum, val):
    """
    Try to read a string that matches num.num and return as a float.
    Otherwise return the input as found.
    """
    # Extract what is coming next.
    next_isnum, next_val, next_isuni = iterable.peek(triple_none)

    # If a non-number was given, we can only accept a decimal point.
    if not isnum:

        # If the next value is None or not a non-uni number, return as-is.
        if next_val is None or not next_isnum or next_isuni:
            yield val

        # If this the decimal point, add it to the number and return.
        elif val == '.':
            next(iterable)  # To progress the iterator.
            yield [val, next_val]

        # If the val ends with the decimal point, split the decimal point
        # off the end of the string then place it to the front of the
        # iterable so that we can use it later.
        elif val.endswith('.'):
            iterable.push(SplitElement(False, val[-1], False))
            yield val[:-1]

        # Otherwise, just return the val and move on.
        else:
            yield val

    # If a number, read the number then try to get the post-decimal part.
    else:

        # If the next element is not '.', return now.
        if next_val != '.':
            # If the next val starts with a '.', let's add that.
            if next_val is not None and next_val.startswith('.'):
                next(iterable)  # To progress the iterator.
                iterable.push(SplitElement(False, next_val[1:], False))
                yield [val, next_val[0]]
            else:
                yield [val]

        # Recursively parse the decimal and after. If the returned
        # value is a list, add the list to the current number.
        # If not, just return the number with the decimal.
        else:
            # If the first value returned from the try_to_read_float
            # is a list, add it to the float component list.
            next(iterable)  # To progress the iterator.
            ret = next(try_to_read_float(iterable, next_isnum, next_val))
            if isinstance(ret, list):
                yield [val] + ret
            else:
                yield [val, next_val]


def try_to_read_float_with_exp(iterable, isnum, val):
    """
    Try to read a string that matches num.numE[+-]num and return as a float.
    Otherwise return the input as found.
    """
    exp_ident = ('e', 'E', 'e-', 'E-', 'e+', 'E+')

    # Start by reading the floating point part.
    float_ret = next(try_to_read_float(iterable, isnum, val))

    # Extract what is coming next.
    next_isnum, next_val, next_isuni = iterable.peek(triple_none)

    # If the float part is not a list, or the next value
    # is not in the exponential identifier list, return it as-is.
    if not isinstance(float_ret, list) or next_val not in exp_ident:
        yield float_ret

    # We know the next_val is an exponential identifier. See if the value
    # after that is a non-unicode number. If so, return all as a float.
    # If not, put the exponential identifier back on the front of the
    # list and return the float_ret as-is.
    else:
        exp = SplitElement(next_isnum, next_val, next_isuni)
        next(iterable)  # To progress the iterator.
        next_isnum, next_val, next_isuni = iterable.peek(triple_none)
        if next_isnum and not next_isuni:
            next(iterable)  # To progress the iterator.
            yield float_ret + [exp.val, next_val]
        else:
            iterable.push(exp)
            yield float_ret


def try_to_read_signed_float_template(iterable, isnum, val, key):
    """
    Try to read a string that matches [+-]num.numE[+-]num and return as a
    float. Otherwise return the input as found.
    """
    # Extract what is coming next.
    next_isnum, next_val, next_isuni = iterable.peek(triple_none)

    # If it looks like there is a sign here and the next value is a
    # non-unicode number, try to parse that with the sign.
    if val.endswith(('+', '-')) and next_isnum and not next_isuni:

        # If this value is a sign, return the combo.
        if val in ('+', '-'):
            next(iterable)  # To progress the iterator.
            yield [val] + next(key(iterable, next_isnum, next_val))

        # If the val ends with the sign split the sign off the end of
        # the string then place it to the front of the iterable so that
        # we can use it later.
        else:
            iterable.push(SplitElement(False, val[-1], False))
            yield val[:-1]

    # If it looks like there is a sign here and the next value is a
    # decimal, try to parse as a decimal.
    elif val.endswith(('+.', '-.')) and next_isnum and not next_isuni:

        # Push back a zero before the decimal then parse.
        print(val, iterable.peek())

        # If this value is a sign, return the combo
        if val[:-1] in ('+', '-'):
            yield [val[:-1]] + next(key(iterable, False, val[-1]))

        # If the val ends with the sign split the decimal the end of
        # the string then place it to the front of the iterable so that
        # we can use it later.
        else:
            iterable.push(SplitElement(False, val[-2:], False))
            yield val[:-2]

    # If no sign, pass directly to the key function.
    else:
        yield next(key(iterable, isnum, val))


def add_leading_space_if_first_is_num(iterable, sep):
    """Check if the first element is a number, and prepend with space if so."""
    z, peek = itertools.tee(iterable)
    if type(next(peek, None)) in (int, long, float):
        z = itertools.chain([sep], z)
    del peek
    return z


def sep_inserter(iterable, sep, types=frozenset((int, long, float))):
    """Simulates the py3_safe function."""
    pairs = pairwise(iterable)

    # Prime loop by handling first pair specially.
    first, second = next(pairs)
    if second is None:  # Only one element
        yield first
    elif type(first) in types and type(second) in types:
        yield first
        yield sep
        yield second
    else:
        yield first
        yield second

    # Handle all remaining pairs in loop.
    for first, second in pairs:
        if type(first) in types and type(second) in types:
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


class peekable(object):
    """Wrapper for an iterator to allow 1-item lookahead
    Call ``peek()`` on the result to get the value that will next pop out of
    ``next()``, without advancing the iterator:
        >>> p = peekable(xrange(2))
        >>> p.peek()
        0
        >>> p.next()
        0
        >>> p.peek()
        1
        >>> p.next()
        1
    Pass ``peek()`` a default value, and it will be returned in the case where
    the iterator is exhausted:
        >>> p = peekable([])
        >>> p.peek('hi')
        'hi'
    If no default is provided, ``peek()`` raises ``StopIteration`` when there
    are no items left.
    To test whether there are more items in the iterator, examine the
    peekable's truth value. If it is truthy, there are more items.
        >>> assert peekable(xrange(1))
        >>> assert not peekable([])
    """
    # Lowercase to blend in with itertools. The fact that it's a class is an
    # implementation detail.

    def __init__(self, iterable):
        self._it = iter(iterable)

    def __iter__(self):
        return self

    def __nonzero__(self):
        try:
            self.peek()
        except StopIteration:
            return False
        return True

    __bool__ = __nonzero__

    def peek(self, default=_sentinel):
        """Return the item that will be next returned from ``next()``.
        Return ``default`` if there are no items left. If ``default`` is not
        provided, raise ``StopIteration``.
        """
        if not hasattr(self, '_peek'):
            try:
                self._peek = next(self._it)
            except StopIteration:
                if default is _sentinel:
                    raise
                return default
        return self._peek

    def next(self):
        ret = self.peek()
        try:
            del self._peek
        except AttributeError:
            pass
        return ret

    __next__ = next

    def push(self, value):
        """Put an element at the front of the iterable."""
        if hasattr(self, '_peek'):
            self._it = itertools.chain([value, self._peek], self._it)
            del self._peek
        else:
            self._it = itertools.chain([value], self._it)
