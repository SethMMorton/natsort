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

from __future__ import (print_function, division,
                        unicode_literals, absolute_import)

import re
from os import curdir, pardir
from os.path import split, splitext
from operator import itemgetter
from functools import partial
from itertools import islice
from warnings import warn

# If the user has fastnumbers installed, they will get great speed
# benefits.  If not, we simulate the functions here.
try:
    from fastnumbers import fast_float, fast_int, isreal
except ImportError:
    from .fake_fastnumbers import fast_float, fast_int, isreal

from .py23compat import u_format, py23_str, py23_zip

# Make sure the doctest works for either python2 or python3
__doc__ = u_format(__doc__)

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
    (float, True,  True):  (float_sign_exp_re,     fast_float),
    (float, True,  False): (float_sign_noexp_re,   fast_float),
    (float, False, True):  (float_nosign_exp_re,   fast_float),
    (float, False, False): (float_nosign_noexp_re, fast_float),
    (int,   True,  True):  (int_sign_re,   fast_int),
    (int,   True,  False): (int_sign_re,   fast_int),
    (int,   False, True):  (int_nosign_re, fast_int),
    (int,   False, False): (int_nosign_re, fast_int),
    (None,  True,  True):  (int_nosign_re, fast_int),
    (None,  True,  False): (int_nosign_re, fast_int),
    (None,  False, True):  (int_nosign_re, fast_int),
    (None,  False, False): (int_nosign_re, fast_int),
}


def _number_finder(s, regex, numconv, py3_safe):
    """Helper to split numbers"""

    # Split the input string by numbers. If there are no splits, return now.
    # If the input is not a string, TypeError is raised.
    s = regex.split(s)
    if len(s) == 1:
        return tuple(s)

    # Now convert the numbers to numbers, and leave strings as strings.
    # Remove empty strings from the list.
    s = [numconv(x) for x in s if x]

    # If the list begins with a number, lead with an empty string.
    # This is used to get around the "unorderable types" issue.
    if isreal(s[0]):
        s = [''] + s

    # The _py3_safe function inserts "" between numbers in the list,
    # and is used to get around "unorderable types" in complex cases.
    # It is a separate function that needs to be requested specifically
    # because it is expensive to call.
    return _py3_safe(s) if py3_safe else s


def _path_splitter(s, _d_match=re.compile(r'\.\d').match):
    """Split a string into its path components. Assumes a string is a path."""
    path_parts = []
    p_append = path_parts.append
    path_location = s

    # Continue splitting the path from the back until we have reached
    # '..' or '.', or until there is nothing left to split.
    while path_location != curdir and path_location != pardir:
        parent_path = path_location
        path_location, child_path = split(parent_path)
        if path_location == parent_path:
            break
        p_append(child_path)

    # This last append is the base path.
    # Only append if the string is non-empty.
    if path_location:
        p_append(path_location)

    # We created this list in reversed order, so we now correct the order.
    path_parts.reverse()

    # Now, split off the file extensions using a similar method to above.
    # Continue splitting off file extensions until we reach a decimal number
    # or there are no more extensions.
    base = path_parts.pop()
    base_parts = []
    b_append = base_parts.append
    while True:
        front = base
        base, ext = splitext(front)
        if _d_match(ext) or not ext:
            # Reset base to before the split if the split is invalid.
            base = front
            break
        b_append(ext)
    b_append(base)
    base_parts.reverse()

    # Return the split parent paths and then the split basename.
    return path_parts + base_parts


def _py3_safe(parsed_list):
    """Insert '' between two numbers."""
    length = len(parsed_list)
    if length < 2:
        return parsed_list
    else:
        new_list = [parsed_list[0]]
        nl_append = new_list.append
        for before, after in py23_zip(islice(parsed_list, 0, length-1),
                                      islice(parsed_list, 1, None)):
            if isreal(before) and isreal(after):
                nl_append("")
            nl_append(after)
        return new_list


def _natsort_key(val, key=None, number_type=float, signed=True, exp=True,
                 as_path=False, py3_safe=False):
    """\
    Key to sort strings and numbers naturally.

    It works by separating out the numbers from the strings. This function for
    internal use only. See the natsort_keygen documentation for details of each
    parameter.

    Parameters
    ----------
    val : {str, unicode}
    key : callable, optional
    number_type : {None, float, int}, optional
    signed : {True, False}, optional
    exp : {True, False}, optional
    as_path : {True, False}, optional
    py3_safe : {True, False}, optional

    Returns
    -------
    out : tuple
        The modified value with numbers extracted.

    """

    # Convert the arguments to the proper input tuple
    inp_options = (number_type, signed, exp)
    try:
        regex, num_function = regex_and_num_function_chooser[inp_options]
    except KeyError:
        # Report errors properly
        if number_type not in (float, int) and number_type is not None:
            raise ValueError("_natsort_key: 'number_type' parameter "
                             "'{0}' invalid".format(py23_str(number_type)))
        elif signed not in (True, False):
            raise ValueError("_natsort_key: 'signed' parameter "
                             "'{0}' invalid".format(py23_str(signed)))
        elif exp not in (True, False):
            raise ValueError("_natsort_key: 'exp' parameter "
                             "'{0}' invalid".format(py23_str(exp)))
    else:
        # Apply key if needed.
        if key is not None:
            val = key(val)

        # If this is a path, convert it.
        # An AttrubuteError is raised if not a string.
        split_as_path = False
        if as_path:
            try:
                val = _path_splitter(val)
            except AttributeError:
                pass
            else:
                # Record that this string was split as a path so that
                # we can set as_path to False in the recursive call.
                split_as_path = True

        # Assume the input are strings, which is the most common case.
        try:
            return tuple(_number_finder(val, regex, num_function, py3_safe))
        except TypeError:
            # If not strings, assume it is an iterable that must
            # be parsed recursively. Do not apply the key recursively.
            # If this string was split as a path, set as_path to False.
            try:
                return tuple([_natsort_key(x, None, number_type, signed,
                                           exp, as_path and not split_as_path,
                                           py3_safe) for x in val])
            # If there is still an error, it must be a number.
            # Return as-is, with a leading empty string.
            # Waiting for two raised errors instead of calling
            # isinstance at the opening of the function is slower
            # for numbers but much faster for strings, and since
            # numbers are not a common input to natsort this is
            # an acceptable sacrifice.
            except TypeError:
                return (('', val,),) if as_path else ('', val,)


@u_format
def natsort_key(val, key=None, number_type=float, signed=True, exp=True,
                as_path=False, py3_safe=False):
    """\
    Key to sort strings and numbers naturally.

    Key to sort strings and numbers naturally, not lexicographically.
    It is designed for use in passing to the 'sorted' builtin or
    'sort' attribute of lists.

    .. note:: Depreciated since version 3.4.0.
              This function remains in the publicly exposed API for
              backwards-compatibility reasons, but future development
              should use the newer `natsort_keygen` function. It is
              planned to remove this from the public API in natsort
              version 4.0.0.  A DeprecationWarning will be raised
              via the warnings module; set warnings.simplefilter("always")
              to raise them to see if your code will work in version
              4.0.0.

    Parameters
    ----------
    val : {{str, unicode}}
        The value used by the sorting algorithm

    key : callable, optional
        A key used to manipulate the input value before parsing for
        numbers. It is **not** applied recursively.
        It should accept a single argument and return a single value.

    number_type : {{None, float, int}}, optional
        The types of number to sort on: `float` searches for floating
        point numbers, `int` searches for integers, and `None` searches
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

    as_path : {{True, False}}, optional
        This option will force strings to be interpreted as filesystem
        paths, so they will be split according to the filesystem separator
        (i.e. '/' on UNIX, '\\\\' on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder', 'Folder (1)', 'Folder (10)']`` will not be sorted
        properly; ``'Folder'`` will be placed at the end, not at the front.
        The default behavior is `as_path = False`.

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
    msg = "natsort_key is depreciated as of 3.4.0, please use natsort_keygen"
    warn(msg, DeprecationWarning)
    return _natsort_key(val, key, number_type, signed, exp, as_path, py3_safe)


@u_format
def natsort_keygen(key=None, number_type=float, signed=True, exp=True,
                   as_path=False, py3_safe=False):
    """\
    Generate a key to sort strings and numbers naturally.

    Generate a key to sort strings and numbers naturally,
    not lexicographically. This key is designed for use as the
    `key` argument to functions such as the `sorted` builtin.

    The user may customize the generated function with the
    arguments to `natsort_keygen`, including an optional
    `key` function which will be called before the `natsort_key`.

    Parameters
    ----------
    key : callable, optional
        A key used to manipulate the input value before parsing for
        numbers. It is **not** applied recursively.
        It should accept a single argument and return a single value.

    number_type : {{None, float, int}}, optional
        The types of number to sort on: `float` searches for floating
        point numbers, `int` searches for integers, and `None` searches
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

    as_path : {{True, False}}, optional
        This option will force strings to be interpreted as filesystem
        paths, so they will be split according to the filesystem separator
        (i.e. `/` on UNIX, `\\\\` on Windows), as well as splitting on the
        file extension, if any. Without this, lists with file paths like
        ``['Folder/', 'Folder (1)/', 'Folder (10)/']`` will not be sorted
        properly; ``'Folder'`` will be placed at the end, not at the front.
        The default behavior is `as_path = False`.

    py3_safe : {{True, False}}, optional
        This will make the string parsing algorithm be more careful by
        placing an empty string between two adjacent numbers after the
        parsing algorithm. This will prevent the "unorderable types"
        error.

    Returns
    -------
    out : function
        A wrapped version of the `natsort_key` function that is
        suitable for passing as the `key` argument to functions
        such as `sorted`.

    Examples
    --------
    `natsort_keygen` is a convenient waynto create a custom key
    to sort lists in-place (for example). Calling with no objects
    will return a plain `natsort_key` instance::

        >>> a = ['num5.10', 'num-3', 'num5.3', 'num2']
        >>> b = a[:]
        >>> a.sort(key=natsort_key)
        >>> b.sort(key=natsort_keygen())
        >>> a == b
        True

    The power of `natsort_keygen` is when you want to want to pass
    arguments to the `natsort_key`.  Consider the following
    equivalent examples; which is more clear? ::

        >>> a = ['num5.10', 'num-3', 'num5.3', 'num2']
        >>> b = a[:]
        >>> a.sort(key=lambda x: natsort_key(x, key=lambda y: y.upper(),
        ...        signed=False))
        >>> b.sort(key=natsort_keygen(key=lambda x: x.upper(), signed=False))
        >>> a == b
        True

    """
    return partial(_natsort_key,
                   key=key,
                   number_type=number_type,
                   signed=signed,
                   exp=exp,
                   as_path=as_path,
                   py3_safe=py3_safe)


@u_format
def natsorted(seq, key=None, number_type=float, signed=True, exp=True,
              reverse=False, as_path=False):
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
        point numbers, `int` searches for integers, and `None` searches
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

    reverse : {{True, False}}, optional
        Return the list in reversed sorted order. The default is
        `False`.

    as_path : {{True, False}}, optional
        This option will force strings to be interpreted as filesystem
        paths, so they will be split according to the filesystem separator
        (i.e. '/' on UNIX, '\\\\' on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder', 'Folder (1)', 'Folder (10)']`` will not be sorted
        properly; ``'Folder'`` will be placed at the end, not at the front.
        The default behavior is `as_path = False`.

    Returns
    -------
    out: list
        The sorted sequence.

    See Also
    --------
    natsort_keygen : Generates the key that makes natural sorting possible.
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
        return sorted(seq, reverse=reverse,
                      key=natsort_keygen(key, number_type,
                                         signed, exp, as_path))
    except TypeError as e:
        # In the event of an unresolved "unorderable types" error
        # attempt to sort again, being careful to prevent this error.
        if 'unorderable types' in str(e):
            return sorted(seq, reverse=reverse,
                          key=natsort_keygen(key, number_type,
                                             signed, exp, as_path,
                                             True))
        else:
            # Re-raise if the problem was not "unorderable types"
            raise


@u_format
def versorted(seq, key=None, reverse=False, as_path=False):
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

    reverse : {{True, False}}, optional
        Return the list in reversed sorted order. The default is
        `False`.

    as_path : {{True, False}}, optional
        This option will force strings to be interpreted as filesystem
        paths, so they will be split according to the filesystem separator
        (i.e. '/' on UNIX, '\\\\' on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder', 'Folder (1)', 'Folder (10)']`` will not be sorted
        properly; ``'Folder'`` will be placed at the end, not at the front.
        The default behavior is `as_path = False`.

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
    return natsorted(seq, key, None, reverse=reverse, as_path=as_path)


@u_format
def index_natsorted(seq, key=None, number_type=float, signed=True, exp=True,
                    reverse=False, as_path=False):
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
        point numbers, `int` searches for integers, and `None` searches
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

    reverse : {{True, False}}, optional
        Return the list in reversed sorted order. The default is
        `False`.

    as_path : {{True, False}}, optional
        This option will force strings to be interpreted as filesystem
        paths, so they will be split according to the filesystem separator
        (i.e. '/' on UNIX, '\\\\' on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder', 'Folder (1)', 'Folder (10)']`` will not be sorted
        properly; ``'Folder'`` will be placed at the end, not at the front.
        The default behavior is `as_path = False`.

    Returns
    -------
    out : tuple
        The ordered indexes of the sequence.

    See Also
    --------
    natsorted
    order_by_index

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
        >>> order_by_index(a, index)
        [{u}'num2', {u}'num3', {u}'num5']
        >>> order_by_index(b, index)
        [{u}'baz', {u}'foo', {u}'bar']

    """
    if key is None:
        newkey = itemgetter(1)
    else:
        newkey = lambda x: key(itemgetter(1)(x))
    # Pair the index and sequence together, then sort by element
    index_seq_pair = [[x, y] for x, y in enumerate(seq)]
    try:
        index_seq_pair.sort(reverse=reverse,
                            key=natsort_keygen(newkey, number_type,
                                               signed, exp, as_path))
    except TypeError as e:
        # In the event of an unresolved "unorderable types" error
        # attempt to sort again, being careful to prevent this error.
        if 'unorderable types' in str(e):
            index_seq_pair.sort(reverse=reverse,
                                key=natsort_keygen(newkey, number_type,
                                                   signed, exp, as_path,
                                                   True))
        else:
            # Re-raise if the problem was not "unorderable types"
            raise
    return [x for x, _ in index_seq_pair]


@u_format
def index_versorted(seq, key=None, reverse=False, as_path=False):
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

    reverse : {{True, False}}, optional
        Return the list in reversed sorted order. The default is
        `False`.

    as_path : {{True, False}}, optional
        This option will force strings to be interpreted as filesystem
        paths, so they will be split according to the filesystem separator
        (i.e. '/' on UNIX, '\\\\' on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder', 'Folder (1)', 'Folder (10)']`` will not be sorted
        properly; ``'Folder'`` will be placed at the end, not at the front.
        The default behavior is `as_path = False`.

    Returns
    -------
    out : tuple
        The ordered indexes of the sequence.

    See Also
    --------
    versorted
    order_by_index

    Examples
    --------
    Use `index_versorted` just like the builtin `sorted`::

        >>> a = ['num4.0.2', 'num3.4.1', 'num3.4.2']
        >>> index_versorted(a)
        [1, 2, 0]

    """
    return index_natsorted(seq, key, None, reverse=reverse, as_path=as_path)


@u_format
def order_by_index(seq, index, iter=False):
    """\
    Order a given sequence by an index sequence.

    The output of `index_natsorted` and `index_versorted` is a
    sequence of integers (index) that correspond to how its input
    sequence **would** be sorted. The idea is that this index can
    be used to reorder multiple sequences by the sorted order of the
    first sequence. This function is a convenient wrapper to
    apply this ordering to a sequence.

    Parameters
    ----------
    seq : iterable
        The sequence to order.

    index : iterable
        The sequence that indicates how to order `seq`.
        It should be the same length as `seq` and consist
        of integers only.

    iter : {{True, False}}, optional
        If `True`, the ordered sequence is returned as a
        generator expression; otherwise it is returned as a
        list. The default is `False`.

    Returns
    -------
    out : {{list, generator}}
        The sequence ordered by `index`, as a `list` or as a
        generator expression (depending on the value of `iter`).

    See Also
    --------
    index_natsorted
    index_versorted

    Examples
    --------

    `order_by_index` is a comvenience function that helps you apply
    the result of `index_natsorted` or `index_versorted`::

        >>> a = ['num3', 'num5', 'num2']
        >>> b = ['foo', 'bar', 'baz']
        >>> index = index_natsorted(a)
        >>> index
        [2, 0, 1]
        >>> # Sort both lists by the sort order of a
        >>> order_by_index(a, index)
        [{u}'num2', {u}'num3', {u}'num5']
        >>> order_by_index(b, index)
        [{u}'baz', {u}'foo', {u}'bar']

    """
    return (seq[i] for i in index) if iter else [seq[i] for i in index]
