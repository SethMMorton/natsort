# -*- coding: utf-8 -*-
"""
Natsort can sort strings with numbers in a natural order.
It provides the natsorted function to sort strings with
arbitrary numbers.

You can mix types with natsorted.  This can get around the new
'unorderable types' issue with Python 3. Natsort will recursively
descend into lists of lists so you can sort by the sublist contents.

See the README or the natsort homepage for more details.

"""

from __future__ import print_function, division, unicode_literals, absolute_import

import re
import sys
from operator import itemgetter
from numbers import Number
from itertools import islice

from .py23compat import u_format, py23_basestring, py23_range, py23_str, py23_zip

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


def _remove_empty(s):
    """Remove empty strings from a list."""
    while True:
        try:
            s.remove('')
        except ValueError:
            break
    return s


def _number_finder(s, regex, numconv, py3_safe):
    """Helper to split numbers"""

    # Split.  If there are no splits, return now
    s = regex.split(s)
    if len(s) == 1:
        return tuple(s)

    # Now convert the numbers to numbers, and leave strings as strings
    s = _remove_empty(s)
    for i in py23_range(len(s)):
        try:
            s[i] = numconv(s[i])
        except ValueError:
            pass

    # If the list begins with a number, lead with an empty string.
    # This is used to get around the "unorderable types" issue.
    # The _py3_safe function inserts "" between numbers in the list,
    # and is used to get around "unorderable types" in complex cases.
    # It is a separate function that needs to be requested specifically
    # because it is expensive to call.
    if not isinstance(s[0], py23_basestring):
        return _py3_safe([''] + s) if py3_safe else [''] + s
    else:
        return _py3_safe(s) if py3_safe else s


def _py3_safe(parsed_list):
    """Insert '' between two numbers."""
    if len(parsed_list) < 2:
        return parsed_list
    else:
        new_list = [parsed_list[0]]
        nl_append = new_list.append
        for before, after in py23_zip(islice(parsed_list, 0, len(parsed_list)-1),
                                      islice(parsed_list, 1, None)):
            if isinstance(before, Number) and isinstance(after, Number):
                nl_append("")
            nl_append(after)
        return new_list


@u_format
def natsort_key(s, number_type=float, signed=True, exp=True, py3_safe=False):
    """\
    Key to sort strings and numbers naturally.

    Key to sort strings and numbers naturally, not lexicographically.
    It is designed for use in passing to the 'sorted' builtin or
    'sort' attribute of lists.

    .. note:: Depreciation Notice (3.3.1)
              This function remains in the publicly exposed API for
              backwards-compatibility reasons, but future development
              should use the newer `natsort_keygen` function. There
              are no plans to officially remove this method from the
              public API, but it leads to messier code than using
              `natsort_keygen` so the latter should be preferred.

    Parameters
    ----------
    val : {{str, unicode}}
        The value used by the sorting algorithm

    number_type : {{None, float, int}}, optional
        The types of number to sort on: `float` searches for floating
        point numbers, `int` searches for integers, and `None `searches
        for digits (like integers but does not take into account
        negative sign). `None` is a shortcut for `number_type = int`
        and `signed = False`.

    signed : {{True, False}}, optional
        By default a '+' or '-' before a number is taken to be the sign
        of the number. If `signed` is `False`, any '+' or '-' will not
        be considered to be part of the number, but as part part of the
        string.

    exp : {{True, False}}, optional
        This option only applies to `number_type = float`.  If
        `exp = True`, a string like "3.5e5" will be interpreted as
        350000, i.e. the exponential part is considered to be part of
        the number. If `exp = False`, "3.5e5" is interpreted as
        ``(3.5, "e", 5)``. The default behavior is `exp = True`.

    py3_safe : {{True, False}}, optional
        This will make the string parsing algorithm be more careful by
        placing an empty string between two adjacent numbers after the
        parsing algorithm. This will prevent the "unorderable types"
        error.

    Returns
    -------
    out : tuple
        The modified value with numbers extracted.

    See Also
    --------
    natsort_keygen : Generates a properly wrapped `natsort_key`.

    Examples
    --------
    Using natsort_key is just like any other sorting key in python::

        >>> a = ['num3', 'num5', 'num2']
        >>> a.sort(key=natsort_key)
        >>> a
        [{u}'num2', {u}'num3', {u}'num5']

    It works by separating out the numbers from the strings::

        >>> natsort_key('num2')
        ({u}'num', 2.0)

    If you need to call natsort_key with the number_type argument, or get a
    special attribute or item of each element of the sequence, please use
    the `natsort_keygen` function.  Actually, please just use the
    `natsort_keygen` function.

    Notes
    -----
    Iterables are parsed recursively so you can sort lists of lists::

        >>> natsort_key(('a1', 'a10'))
        (({u}'a', 1.0), ({u}'a', 10.0))

    Strings that lead with a number get an empty string at the front of the
    tuple. This is designed to get around the "unorderable types" issue of
    Python3::

        >>> natsort_key('15a')
        ({u}'', 15.0, {u}'a')

    You can give bare numbers, too::

        >>> natsort_key(10)
        ({u}'', 10)

    If you have a case where one of your string has two numbers in a row,
    you can turn on the "py3_safe" option to try to add a "" between sets
    of two numbers::

        >>> natsort_key('43h7+3', py3_safe=True)
        ({u}'', 43.0, {u}'h', 7.0, {u}'', 3.0)

    """

    # If we are dealing with non-strings, return now
    if not isinstance(s, py23_basestring):
        if hasattr(s, '__getitem__'):
            return tuple(natsort_key(x) for x in s)
        else:
            return ('', s,)

    # Convert to the proper tuple and return
    inp_options = (number_type, signed, exp)
    try:
        args = (s,) + regex_and_num_function_chooser[inp_options] + (py3_safe,)
    except KeyError:
        # Report errors properly
        if number_type not in (float, int) and number_type is not None:
            raise ValueError("natsort_key: 'number_type' "
                             "parameter '{0}' invalid".format(py23_str(number_type)))
        elif signed not in (True, False):
            raise ValueError("natsort_key: 'signed' "
                             "parameter '{0}' invalid".format(py23_str(signed)))
        elif exp not in (True, False):
            raise ValueError("natsort_key: 'exp' "
                             "parameter '{0}' invalid".format(py23_str(exp)))
    else:
        return tuple(_number_finder(*args))


@u_format
def natsorted(seq, key=lambda x: x, number_type=float, signed=True, exp=True):
    """\
    Sorts a sequence naturally.

    Sorts a sequence naturally (alphabetically and numerically),
    not lexicographically. Returns a new copy of the sorted
    sequence as a list.

    Parameters
    ----------
    seq : iterable
        The sequence to sort.

    key : callable, optional
        A key used to determine how to sort each element of the sequence.
        It is **not** applied recursively.
        It should accept a single argument and return a single value.

    number_type : {{None, float, int}}, optional
        The types of number to sort on: `float` searches for floating
        point numbers, `int` searches for integers, and `None `searches
        for digits (like integers but does not take into account
        negative sign). `None` is a shortcut for `number_type = int`
        and `signed = False`.

    signed : {{True, False}}, optional
        By default a '+' or '-' before a number is taken to be the sign
        of the number. If `signed` is `False`, any '+' or '-' will not
        be considered to be part of the number, but as part part of the
        string.

    exp : {{True, False}}, optional
        This option only applies to `number_type = float`.  If
        `exp = True`, a string like "3.5e5" will be interpreted as
        350000, i.e. the exponential part is considered to be part of
        the number. If `exp = False`, "3.5e5" is interpreted as
        ``(3.5, "e", 5)``. The default behavior is `exp = True`.

    Returns
    -------
    out: list
        The sorted sequence.

    See Also
    --------
    versorted : A wrapper for ``natsorted(seq, number_type=None)``.
    index_natsorted : Returns the sorted indexes from `natsorted`.

    Examples
    --------
    Use `natsorted` just like the builtin `sorted`::

        >>> a = ['num3', 'num5', 'num2']
        >>> natsorted(a)
        [{u}'num2', {u}'num3', {u}'num5']

    """
    try:
        return sorted(seq, key=lambda x: natsort_key(key(x),
                                                     number_type=number_type,
                                                     signed=signed, exp=exp))
    except TypeError as e:
        # In the event of an unresolved "unorderable types" error
        # attempt to sort again, being careful to prevent this error.
        if 'unorderable types' in str(e):
            return sorted(seq, key=lambda x: natsort_key(key(x),
                                                         number_type=number_type,
                                                         signed=signed, exp=exp,
                                                         py3_safe=True))
        else:
            # Re-raise if the problem was not "unorderable types"
            raise


@u_format
def versorted(seq, key=lambda x: x):
    """\
    Convenience function to sort version numbers.

    Convenience function to sort version numbers. This is a wrapper
    around ``natsorted(seq, number_type=None)``.

    Parameters
    ----------
    seq : iterable
        The sequence to sort.

    key : callable, optional
        A key used to determine how to sort each element of the sequence.
        It is **not** applied recursively.
        It should accept a single argument and return a single value.

    Returns
    -------
    out : list
        The sorted sequence.

    See Also
    --------
    index_versorted : Returns the sorted indexes from `versorted`.

    Examples
    --------
    Use `versorted` just like the builtin `sorted`::

        >>> a = ['num4.0.2', 'num3.4.1', 'num3.4.2']
        >>> versorted(a)
        [{u}'num3.4.1', {u}'num3.4.2', {u}'num4.0.2']

    """
    return natsorted(seq, key=key, number_type=None)


@u_format
def index_natsorted(seq, key=lambda x: x, number_type=float, signed=True, exp=True):
    """\
    Return the list of the indexes used to sort the input sequence.

    Sorts a sequence naturally, but returns a list of sorted the
    indexes and not the sorted list. This list of indexes can be
    used to sort multiple lists by the sorted order of the given
    sequence.

    Parameters
    ----------
    seq : iterable
        The sequence to sort.

    key : callable, optional
        A key used to determine how to sort each element of the sequence.
        It is **not** applied recursively.
        It should accept a single argument and return a single value.

    number_type : {{None, float, int}}, optional
        The types of number to sort on: `float` searches for floating
        point numbers, `int` searches for integers, and `None `searches
        for digits (like integers but does not take into account
        negative sign). `None` is a shortcut for `number_type = int`
        and `signed = False`.

    signed : {{True, False}}, optional
        By default a '+' or '-' before a number is taken to be the sign
        of the number. If `signed` is `False`, any '+' or '-' will not
        be considered to be part of the number, but as part part of the
        string.

    exp : {{True, False}}, optional
        This option only applies to `number_type = float`.  If
        `exp = True`, a string like "3.5e5" will be interpreted as
        350000, i.e. the exponential part is considered to be part of
        the number. If `exp = False`, "3.5e5" is interpreted as
        ``(3.5, "e", 5)``. The default behavior is `exp = True`.

    Returns
    -------
    out : tuple
        The ordered indexes of the sequence.

    See Also
    --------
    natsorted

    Examples
    --------

    Use index_natsorted if you want to sort multiple lists by the
    sorted order of one list::

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

    """
    item1 = itemgetter(1)
    # Pair the index and sequence together, then sort by element
    index_seq_pair = [[x, key(y)] for x, y in py23_zip(py23_range(len(seq)), seq)]
    try:
        index_seq_pair.sort(key=lambda x: natsort_key(item1(x), 
                                                      number_type=number_type,
                                                      signed=signed, exp=exp))
    except TypeError as e:
        # In the event of an unresolved "unorderable types" error
        # attempt to sort again, being careful to prevent this error.
        if 'unorderable types' in str(e):
            index_seq_pair.sort(key=lambda x: natsort_key(item1(x), 
                                                          number_type=number_type,
                                                          signed=signed, exp=exp,
                                                          py3_safe=True))
        else:
            # Re-raise if the problem was not "unorderable types"
            raise
    return [x[0] for x in index_seq_pair]


@u_format
def index_versorted(seq, key=lambda x: x):
    """\
    Return the list of the indexes used to sort the input sequence
    of version numbers.

    Sorts a sequence naturally, but returns a list of sorted the
    indexes and not the sorted list. This list of indexes can be
    used to sort multiple lists by the sorted order of the given
    sequence.

    This is a wrapper around ``index_natsorted(seq, number_type=None)``.

    Parameters
    ----------
    seq: iterable
        The sequence to sort.

    key: callable, optional
        A key used to determine how to sort each element of the sequence.
        It is **not** applied recursively.
        It should accept a single argument and return a single value.

    Returns
    -------
    out : tuple
        The ordered indexes of the sequence.

    See Also
    --------
    versorted

    Examples
    --------
    Use `index_versorted` just like the builtin `sorted`::

        >>> a = ['num4.0.2', 'num3.4.1', 'num3.4.2']
        >>> index_versorted(a)
        [1, 2, 0]

    """
    return index_natsorted(seq, key=key, number_type=None)

