# -*- coding: utf-8 -*-
"""
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.

    >>> a = ['a2', 'a5', 'a9', 'a1', 'a4', 'a10', 'a6']
    >>> sorted(a)
    [{u}'a1', {u}'a10', {u}'a2', {u}'a4', {u}'a5', {u}'a6', {u}'a9']
    >>> natsorted(a)
    [{u}'a1', {u}'a2', {u}'a4', {u}'a5', {u}'a6', {u}'a9', {u}'a10']

Here is an example demonstrating how different options sort the same list.

    >>> a = ['a50', 'a51.', 'a50.31', 'a50.4', 'a5.034e1', 'a50.300']
    >>> sorted(a)
    [{u}'a5.034e1', {u}'a50', {u}'a50.300', {u}'a50.31', {u}'a50.4', {u}'a51.']
    >>> natsorted(a)
    [{u}'a50', {u}'a50.300', {u}'a50.31', {u}'a5.034e1', {u}'a50.4', {u}'a51.']
    >>> natsorted(a, number_type=float, exp=False)
    [{u}'a5.034e1', {u}'a50', {u}'a50.300', {u}'a50.31', {u}'a50.4', {u}'a51.']
    >>> natsorted(a, number_type=int)
    [{u}'a5.034e1', {u}'a50', {u}'a50.4', {u}'a50.31', {u}'a50.300', {u}'a51.']
    >>> natsorted(a, number_type=None)
    [{u}'a5.034e1', {u}'a50', {u}'a50.4', {u}'a50.31', {u}'a50.300', {u}'a51.']

This demonstrates the signed option.  It can account for negative and positive signs.
Turning it off treats the '+' or '-' as part of the string.

    >>> a = ['a-5', 'a7', 'a+2']
    >>> sorted(a)
    [{u}'a+2', {u}'a-5', {u}'a7']
    >>> natsorted(a) # signed=True is default, -5 comes first on the number line
    [{u}'a-5', {u}'a+2', {u}'a7']
    >>> natsorted(a, signed=False) # 'a' comes before 'a+', which is before 'a-'
    [{u}'a7', {u}'a+2', {u}'a-5']

Sorting version numbers is best with 'number_type=None'.  That is a shortcut
for 'number_type=int, signed=False'

    >>> a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    >>> sorted(a)
    [{u}'1.10.1', {u}'1.11', {u}'1.11.4', {u}'1.9.9a', {u}'1.9.9b']
    >>> natsorted(a)
    [{u}'1.10.1', {u}'1.11', {u}'1.11.4', {u}'1.9.9a', {u}'1.9.9b']
    >>> natsorted(a, number_type=None)
    [{u}'1.9.9a', {u}'1.9.9b', {u}'1.10.1', {u}'1.11', {u}'1.11.4']

You can mix types with natsorted.  This can get around the new
'unorderable types' issue with Python 3.

    >>> import sys
    >>> a = [6, 4.5, '7', u'2.5']
    >>> if sys.version[0] == '3': # Python 3
    ...     try:
    ...         sorted(a)
    ...     except TypeError as e:
    ...         print(e)
    ... else: # Python 2
    ...     # This will get the doctest to work properly while illustrating the point
    ...     if sorted(a) == [4.5, 6, u'2.5', '7']:
    ...         print('unorderable types: str() < float()')
    ...
    unorderable types: str() < float()
    >>> natsorted(a)
    [{u}'2.5', 4.5, 6, {u}'7']

"""

from __future__ import unicode_literals
from .py23compat import u_format, py23_basestring, py23_range, py23_str, py23_zip
import re
import sys

__doc__ = u_format(__doc__) # Make sure the doctest works for either python2 or python3

# The regex that locates floats
float_sign_exp_re = re.compile(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')
float_nosign_exp_re = re.compile(r'(\d*\.?\d+(?:[eE][-+]?\d+)?)')
float_sign_noexp_re = re.compile(r'([-+]?\d*\.?\d+)')
float_nosign_noexp_re = re.compile(r'(\d*\.?\d+)')
# Integer regexes
int_nosign_re = re.compile(r'(\d+)')
int_sign_re = re.compile(r'([-+]?\d+)')
# This dict will help select the correct regex and number conversion function.
regex_and_num_function_chooser = {
    (float, True,  True)  : (float_sign_exp_re,     float),
    (float, True,  False) : (float_sign_noexp_re,   float),
    (float, False, True)  : (float_nosign_exp_re,   float),
    (float, False, False) : (float_nosign_noexp_re, float),
    (int,   True,  True)  : (int_sign_re,   int),
    (int,   True,  False) : (int_sign_re,   int),
    (int,   False, True)  : (int_nosign_re, int),
    (int,   False, False) : (int_nosign_re, int),
    (None,  True,  True)  : (int_nosign_re, int),
    (None,  True,  False) : (int_nosign_re, int),
    (None,  False, True)  : (int_nosign_re, int),
    (None,  False, False) : (int_nosign_re, int),
}

@u_format
def remove_empty(s):
    """\
    Remove empty strings from a list.

        >>> a = ['a', 2, '', 'b', '']
        >>> remove_empty(a)
        [{u}'a', 2, {u}'b']

    """
    while True:
        try:
            s.remove('')
        except ValueError:
            break
    return s


def _number_finder(s, regex, numconv):
    """Helper to split numbers"""

    # Split.  If there are no splits, return now
    s = regex.split(s)
    if len(s) == 1:
        return tuple(s)

    # Now convert the numbers to numbers, and leave strings as strings
    s = remove_empty(s)
    for i in py23_range(len(s)):
        try:
            s[i] = numconv(s[i])
        except ValueError:
            pass

    return s


@u_format
def natsort_key(s, number_type=float, signed=True, exp=True):
    """\
    Key to sort strings and numbers naturally, not lexicographically.
    It also has basic support for version numbers.
    For use in passing to the :py:func:`sorted` builtin or
    :py:meth:`sort` attribute of lists.

    Use natsort_key just like any other sorting key.

        >>> a = ['num3', 'num5', 'num2']
        >>> a.sort(key=natsort_key)
        >>> a
        [{u}'num2', {u}'num3', {u}'num5']

    Below illustrates how the key works, and how the different options affect sorting.

        >>> natsort_key('a-5.034e1')
        ({u}'a', -50.34)
        >>> natsort_key('a-5.034e1', number_type=float, signed=True, exp=True)
        ({u}'a', -50.34)
        >>> natsort_key('a-5.034e1', number_type=float, signed=True, exp=False)
        ({u}'a', -5.034, {u}'e', 1.0)
        >>> natsort_key('a-5.034e1', number_type=float, signed=False, exp=True)
        ({u}'a-', 50.34)
        >>> natsort_key('a-5.034e1', number_type=float, signed=False, exp=False)
        ({u}'a-', 5.034, {u}'e', 1.0)
        >>> natsort_key('a-5.034e1', number_type=int)
        ({u}'a', -5, {u}'.', 34, {u}'e', 1)
        >>> natsort_key('a-5.034e1', number_type=int, signed=True)
        ({u}'a', -5, {u}'.', 34, {u}'e', 1)
        >>> natsort_key('a-5.034e1', number_type=int, signed=False)
        ({u}'a-', 5, {u}'.', 34, {u}'e', 1)
        >>> natsort_key('a-5.034e1', number_type=int, exp=False)
        ({u}'a', -5, {u}'.', 34, {u}'e', 1)
        >>> natsort_key('a-5.034e1', number_type=None)
        ({u}'a-', 5, {u}'.', 34, {u}'e', 1)

    This is a demonstration of what number_type=None works.

        >>> natsort_key('a-5.034e1', number_type=None) == natsort_key('a-5.034e1', number_type=None, signed=False)
        True
        >>> natsort_key('a-5.034e1', number_type=None) == natsort_key('a-5.034e1', number_type=None, exp=False)
        True
        >>> natsort_key('a-5.034e1', number_type=None) == natsort_key('a-5.034e1', number_type=int, signed=False)
        True

    """

    # If we are dealing with non-strings, return now
    if not isinstance(s, py23_basestring):
        return (s,)

    # Convert to the proper tuple and return
    inp_options = (number_type, signed, exp)
    args = (s,) + regex_and_num_function_chooser[inp_options]
    try:
        return tuple(_number_finder(*args))
    except KeyError:
        # Report errors properly
        if number_type not in (float, int) or number_type is not None:
            raise ValueError("natsort_key: 'number_type' "
                             "parameter '{0}'' invalid".format(py23_str(number_type)))
        elif signed not in (True, False):
            raise ValueError("natsort_key: 'signed' "
                             "parameter '{0}'' invalid".format(py23_str(signed)))
        elif exp not in (True, False):
            raise ValueError("natsort_key: 'exp' "
                             "parameter '{0}'' invalid".format(py23_str(exp)))


@u_format
def natsorted(seq, key=lambda x: x, number_type=float, signed=True, exp=True):
    """\
    Sorts a sequence naturally (alphabetically and numerically),
    not lexicographically.

        >>> a = ['num3', 'num5', 'num2']
        >>> natsorted(a)
        [{u}'num2', {u}'num3', {u}'num5']
        >>> b = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
        >>> from operator import itemgetter
        >>> natsorted(b, key=itemgetter(1))
        [({u}'c', {u}'num2'), ({u}'a', {u}'num3'), ({u}'b', {u}'num5')]

    """
    return sorted(seq, key=lambda x: natsort_key(key(x),
                                                 number_type=number_type,
                                                 signed=signed, exp=exp))


@u_format
def index_natsorted(seq, key=lambda x: x, number_type=float, signed=True, exp=True):
    """\
    Sorts a sequence naturally, but returns a list of sorted the
    indeces and not the sorted list.

        >>> a = ['num3', 'num5', 'num2']
        >>> b = ['foo', 'bar', 'baz']
        >>> index = index_natsorted(a)
        >>> index
        [2, 0, 1]
        >>> # Sort both lists by the sort order of a
        >>> [a[i] for i in index]
        [{u}'num2', {u}'num3', {u}'num5']
        >>> [b[i] for i in index]
        [{u}'baz', {u}'foo', {u}'bar']
        >>> c = [('a', 'num3'), ('b', 'num5'), ('c', 'num2')]
        >>> from operator import itemgetter
        >>> index_natsorted(c, key=itemgetter(1))
        [2, 0, 1]

    """
    from operator import itemgetter
    item1 = itemgetter(1)
    # Pair the index and sequence together, then sort by
    index_seq_pair = [[x, key(y)] for x, y in py23_zip(py23_range(len(seq)), seq)]
    index_seq_pair.sort(key=lambda x: natsort_key(item1(x), 
                                                  number_type=number_type,
                                                  signed=signed, exp=exp))
    return [x[0] for x in index_seq_pair]


def test():
    from doctest import DocTestSuite
    return DocTestSuite()


# Test this module
if __name__ == '__main__':
    import doctest
    doctest.testmod()
