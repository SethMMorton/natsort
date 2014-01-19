# -*- coding: utf-8 -*-
"""
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.

    >>> a = ['a2', 'a8', 'a7', 'a5', 'a9', 'a1', 'a4', 'a10', 'a3', 'a6']
    >>> sorted(a)
    ['a1', 'a10', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9']
    >>> natsorted(a)
    ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10']

    >>> a = ['a50', 'a51.', 'a50.4', 'a5.034e1', 'a50.300']
    >>> sorted(a)
    ['a5.034e1', 'a50', 'a50.300', 'a50.4', 'a51.']
    >>> natsorted(a)
    ['a50', 'a50.300', 'a5.034e1', 'a50.4', 'a51.']
    >>> natsorted(a, number_type=None)
    ['a5.034e1', 'a50', 'a50.4', 'a50.300', 'a51.']

    >>> a = ['1.9.9a', '1.11', '1.9.9b', '1.11.4', '1.10.1']
    >>> sorted(a)
    ['1.10.1', '1.11', '1.11.4', '1.9.9a', '1.9.9b']
    >>> natsorted(a)
    ['1.10.1', '1.11', '1.11.4', '1.9.9a', '1.9.9b']
    >>> natsorted(a, number_type=None)
    ['1.9.9a', '1.9.9b', '1.10.1', '1.11', '1.11.4']

    >>> a = ['name.1', 'name.101', 'name.01', 'name.200', 'name.21']
    >>> sorted(a)
    ['name.01', 'name.1', 'name.101', 'name.200', 'name.21']
    >>> natsorted(a)
    ['name.01', 'name.1', 'name.101', 'name.200', 'name.21']
    >>> natsorted(a, number_type=None)
    ['name.1', 'name.01', 'name.21', 'name.101', 'name.200']

    >>> a = ['version-2', 'version-20', 'version-4', 'version-1']
    >>> sorted(a)
    ['version-1', 'version-2', 'version-20', 'version-4']
    >>> natsorted(a)
    ['version-20', 'version-4', 'version-2', 'version-1']
    >>> natsorted(a, number_type=int)
    ['version-20', 'version-4', 'version-2', 'version-1']
    >>> natsorted(a, number_type=None)
    ['version-1', 'version-2', 'version-4', 'version-20']

    >>> import sys
    >>> a = [6, 4.5, '7', u'2.5']
    >>> if sys.version[0] == '3':
    ...     try:
    ...         sorted(a)
    ...     except TypeError as e:
    ...         print(e)
    ... else:
    ...     # This will get the doctest to work properly while illustrating the point
    ...     if sorted(a) == [4.5, 6, u'2.5', '7']:
    ...         print('unorderable types: str() < float()')
    ...
    unorderable types: str() < float()
    >>> natsorted(a)
    [u'2.5', 4.5, 6, '7']

"""

from __future__ import unicode_literals
from .py23compat import u_format
import re
import sys
# The regex that locates floats
float_re = re.compile(r'([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)')
# A basic digit splitter
digit_re = re.compile(r'(\d+)')
# Integer regex
int_re = re.compile(r'([-+]?[0-9]+)')

# Python 2 and 3 compatibility - Assume all strings are Unicode in Python 2
# Python 2 and 3 compatibility - Use the range iterator always
# Python 2 and 3 compatibility - Uniform base string type
# Python 2 and 3 compatibility - zip as an iterator
py23_str = str if sys.version[0] == '3' else unicode
py23_range = range if sys.version[0] == '3' else xrange
py23_basestring = str if sys.version[0] == '3' else basestring
if sys.version[0] == '3':
    py23_zip = zip
else:
    import itertools
    py23_zip = itertools.izip


def remove_empty(s):
    """\
    Remove empty strings from a list.

        >>> a = ['a', 2, '', 'b']
        >>> remove_empty(a)
        ['a', 2, 'b']

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


def find_floats(s):
    """\
    Locate all the floats in a string, and return a tuple of
    strings and floats.

        >>> find_floats('name3.5')
        ['name', 3.5]
        >>> find_floats('a5.034e1')
        ['a', 50.34]
        >>> find_floats('b-40.2')
        ['b', -40.2]

    """
    return _number_finder(s, float_re, float)


def find_ints(s):
    """\
    Locate all the ints in a string, and return a tuple of
    strings and ints.

        >>> find_ints('name3.5')
        ['name', 3, '.', 5]
        >>> find_ints('a5.034e1')
        ['a', 5, '.', 34, 'e', 1]
        >>> find_ints('b-40.2')
        ['b', -40, '.', 2]

    """
    return _number_finder(s, int_re, int)


def find_digits(s):
    """\
    Locate all the digits in a string, and return a tuple of
    strings and ints.

        >>> find_digits('name3.5')
        ['name', 3, '.', 5]
        >>> find_digits('a5.034e1')
        ['a', 5, '.', 34, 'e', 1]
        >>> find_digits('b-40.2')
        ['b-', 40, '.', 2]

    """
    return _number_finder(s, digit_re, int)


def natsort_key(s, number_type=float):
    """\
    Key to sort strings and numbers naturally, not by ASCII.
    It also has basic support for version numbers.
    For use in passing to the :py:func:`sorted` builtin or
    :py:meth:`sort` attribute of lists.

        >>> a = ['num3', 'num5', 'num2']
        >>> a.sort(key=natsort_key)
        >>> a
        ['num2', 'num3', 'num5']
        >>> class Foo:
        ...    def __init__(self, bar):
        ...        self.bar = bar
        ...    def __repr__(self):
        ...        return "Foo('{0}')".format(self.bar)
        >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> b.sort(key=lambda x: natsort_key(x.bar))
        >>> b
        [Foo('num2'), Foo('num3'), Foo('num5')]
        >>> from operator import attrgetter
        >>> c = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> f = attrgetter('bar')
        >>> c.sort(key=lambda x: natsort_key(f(x)))
        >>> c
        [Foo('num2'), Foo('num3'), Foo('num5')]

    """

    # If we are dealing with non-strings, return now
    if not isinstance(s, py23_basestring):
        return (s,)

    # Convert to the proper tuple and return
    find_method = {float: find_floats, int: find_ints, None: find_digits}
    try:
        return tuple(find_method[number_type](s))
    except KeyError:
        raise ValueError("natsort_key: 'search' parameter {0} invalid".format(py23_str(number_type)))


def natsorted(seq, key=lambda x: x, number_type=float):
    """\
    Sorts a sequence naturally (alphabetically and numerically),
    not by ASCII.

        >>> a = ['num3', 'num5', 'num2']
        >>> natsorted(a)
        ['num2', 'num3', 'num5']
        >>> class Foo:
        ...    def __init__(self, bar):
        ...        self.bar = bar
        ...    def __repr__(self):
        ...        return "Foo('{0}')".format(self.bar)
        >>> b = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> from operator import attrgetter
        >>> natsorted(b, key=attrgetter('bar'))
        [Foo('num2'), Foo('num3'), Foo('num5')]

    :argument seq:
        The sequence to be sorted.
    :type seq: sequence-like
    :rtype: list
    """
    return sorted(seq, key=lambda x: natsort_key(key(x), number_type=number_type))


def index_natsorted(seq, key=lambda x: x, number_type=float):
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
        ['num2', 'num3', 'num5']
        >>> [b[i] for i in index]
        ['baz', 'foo', 'bar']
        >>> class Foo:
        ...    def __init__(self, bar):
        ...        self.bar = bar
        ...    def __repr__(self):
        ...        return "Foo('{0}')".format(self.bar)
        >>> c = [Foo('num3'), Foo('num5'), Foo('num2')]
        >>> from operator import attrgetter
        >>> index_natsorted(c, key=attrgetter('bar'))
        [2, 0, 1]

    :argument seq:
        The sequence that you want the sorted index of.
    :type seq: sequence-like
    :rtype: list
    """
    from operator import itemgetter
    item1 = itemgetter(1)
    # Pair the index and sequence together, then sort by
    index_seq_pair = [[x, key(y)] for x, y in py23_zip(py23_range(len(seq)), seq)]
    index_seq_pair.sort(key=lambda x: natsort_key(item1(x), number_type=number_type))
    return [x[0] for x in index_seq_pair]


def test():
    from doctest import DocTestSuite
    return DocTestSuite()

# Test this module
if __name__ == '__main__':
    import doctest
    doctest.testmod()
