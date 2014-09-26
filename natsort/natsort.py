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

# Std lib. imports.
from operator import itemgetter
from functools import partial
from warnings import warn

# Local imports.
from natsort.utils import _natsort_key, _args_to_enum
from natsort.ns_enum import ns
from natsort.py23compat import u_format

# Make sure the doctest works for either python2 or python3
__doc__ = u_format(__doc__)


@u_format
def natsort_key(val, key=None, number_type=float, signed=None, exp=None,
                as_path=None, py3_safe=None, alg=0):
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
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    signed : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    exp : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    as_path : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    py3_safe : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

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
    alg = _args_to_enum(number_type, signed, exp, as_path, py3_safe) | alg
    return _natsort_key(val, key, alg)


@u_format
def natsort_keygen(key=None, number_type=float, signed=None, exp=None,
                   as_path=None, py3_safe=None, alg=0):
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
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    signed : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    exp : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    as_path : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    py3_safe : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

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
    alg = _args_to_enum(number_type, signed, exp, as_path, py3_safe) | alg
    return partial(_natsort_key, key=key, alg=alg)


@u_format
def natsorted(seq, key=None, number_type=float, signed=None, exp=None,
              reverse=False, as_path=None, alg=0):
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
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    signed : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    exp : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    reverse : {{True, False}}, optional
        Return the list in reversed sorted order. The default is
        `False`.

    as_path : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

    Returns
    -------
    out: list
        The sorted sequence.

    See Also
    --------
    natsort_keygen : Generates the key that makes natural sorting possible.
    versorted : A wrapper for ``natsorted(seq, alg=ns.VERSION)``.
    humansorted : A wrapper for ``natsorted(seq, alg=ns.LOCALE)``.
    index_natsorted : Returns the sorted indexes from `natsorted`.

    Examples
    --------
    Use `natsorted` just like the builtin `sorted`::

        >>> a = ['num3', 'num5', 'num2']
        >>> natsorted(a)
        [{u}'num2', {u}'num3', {u}'num5']

    """
    alg = _args_to_enum(number_type, signed, exp, as_path, None) | alg
    try:
        return sorted(seq, reverse=reverse,
                      key=natsort_keygen(key, alg=alg))
    except TypeError as e:  # pragma: no cover
        # In the event of an unresolved "unorderable types" error
        # attempt to sort again, being careful to prevent this error.
        if 'unorderable types' in str(e):
            return sorted(seq, reverse=reverse,
                          key=natsort_keygen(key,
                                             alg=alg | ns.TYPESAFE))
        else:
            # Re-raise if the problem was not "unorderable types"
            raise


@u_format
def versorted(seq, key=None, reverse=False, as_path=None, alg=0):
    """\
    Convenience function to sort version numbers.

    Convenience function to sort version numbers. This is a wrapper
    around ``natsorted(seq, alg=ns.VERSION)``.

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
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

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
    alg = _args_to_enum(float, None, None, as_path, None) | alg
    return natsorted(seq, key, reverse=reverse, alg=alg | ns.VERSION)


@u_format
def humansorted(seq, key=None, reverse=False, alg=0):
    """\
    Convenience function to properly sort non-numeric characters.

    Convenience function to properly sort non-numeric characters
    in a locale-aware fashion (a.k.a "human sorting"). This is a
    wrapper around ``natsorted(seq, alg=ns.LOCALE)``.

    .. warning:: On some systems, the underlying C library that
                 Python's locale module uses is broken. On these
                 systems it is recommended that you install
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_.
                 Please validate that this function works as
                 expected on your target system, and if not you
                 should add
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_
                 as a dependency.

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

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

    Returns
    -------
    out : list
        The sorted sequence.

    See Also
    --------
    index_humansorted : Returns the sorted indexes from `humansorted`.

    Notes
    -----
    You may find that if you do not explicitly set
    the locale your results may not be as you expect... I have found that
    it depends on the system you are on. To do this is straightforward
    (in the below example I use 'en_US.UTF-8', but you should use your
    locale)::

        >>> import locale
        >>> # The 'str' call is only to get around a bug on Python 2.x
        >>> # where 'setlocale' does not expect unicode strings (ironic,
        >>> # right?)
        >>> locale.setlocale(locale.LC_ALL, str('en_US.UTF-8'))
        'en_US.UTF-8'

    It is preferred that you do this before importing `natsort`.
    If you use `PyICU <https://pypi.python.org/pypi/PyICU>`_ (see warning
    above) then you should not need to do this.

    Examples
    --------
    Use `humansorted` just like the builtin `sorted`::

        >>> a = ['Apple', 'Banana', 'apple', 'banana']
        >>> natsorted(a)
        [{u}'Apple', {u}'Banana', {u}'apple', {u}'banana']
        >>> humansorted(a)
        [{u}'apple', {u}'Apple', {u}'banana', {u}'Banana']

    """
    return natsorted(seq, key, reverse=reverse, alg=alg | ns.LOCALE)


@u_format
def index_natsorted(seq, key=None, number_type=float, signed=None, exp=None,
                    reverse=False, as_path=None, alg=0):
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
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    signed : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    exp : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    reverse : {{True, False}}, optional
        Return the list in reversed sorted order. The default is
        `False`.

    as_path : {{True, False}}, optional
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

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
    alg = _args_to_enum(number_type, signed, exp, as_path, None) | alg
    if key is None:
        newkey = itemgetter(1)
    else:
        newkey = lambda x: key(itemgetter(1)(x))
    # Pair the index and sequence together, then sort by element
    index_seq_pair = [[x, y] for x, y in enumerate(seq)]
    try:
        index_seq_pair.sort(reverse=reverse,
                            key=natsort_keygen(newkey, alg=alg))
    except TypeError as e:  # pragma: no cover
        # In the event of an unresolved "unorderable types" error
        # attempt to sort again, being careful to prevent this error.
        if 'unorderable types' in str(e):
            index_seq_pair.sort(reverse=reverse,
                                key=natsort_keygen(newkey,
                                                   alg=alg | ns.TYPESAFE))
        else:
            # Re-raise if the problem was not "unorderable types"
            raise
    return [x for x, _ in index_seq_pair]


@u_format
def index_versorted(seq, key=None, reverse=False, as_path=None, alg=0):
    """\
    Return the list of the indexes used to sort the input sequence
    of version numbers.

    Sorts a sequence of version, but returns a list of sorted the
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
        Depreciated as of version 3.5.0 and will become an undocumented
        keyword-only argument in 4.0.0. Please use the `alg` argument
        for all future development. See :class:`ns` class documentation for
        details.

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

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
    alg = _args_to_enum(float, None, None, as_path, None) | alg
    return index_natsorted(seq, key, reverse=reverse, alg=alg | ns.VERSION)


@u_format
def index_humansorted(seq, key=None, reverse=False, alg=0):
    """\
    Return the list of the indexes used to sort the input sequence
    in a locale-aware manner.

    Sorts a sequence in a locale-aware manner, but returns a list
    of sorted the indexes and not the sorted list. This list of
    indexes can be used to sort multiple lists by the sorted order
    of the given sequence.

    This is a wrapper around ``index_natsorted(seq, alg=ns.LOCALE)``.

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

    alg : ns enum, optional
        This option is used to control which algorithm `natsort`
        uses when sorting. For details into these options, please see
        the :class:`ns` class documentation. The default is `ns.FLOAT`.

    Returns
    -------
    out : tuple
        The ordered indexes of the sequence.

    See Also
    --------
    humansorted
    order_by_index

    Notes
    -----
    You may find that if you do not explicitly set
    the locale your results may not be as you expect... I have found that
    it depends on the system you are on. To do this is straightforward
    (in the below example I use 'en_US.UTF-8', but you should use your
    locale)::

        >>> import locale
        >>> # The 'str' call is only to get around a bug on Python 2.x
        >>> # where 'setlocale' does not expect unicode strings (ironic,
        >>> # right?)
        >>> locale.setlocale(locale.LC_ALL, str('en_US.UTF-8'))
        'en_US.UTF-8'

    It is preferred that you do this before importing `natsort`.
    If you use `PyICU <https://pypi.python.org/pypi/PyICU>`_ (see warning
    above) then you should not need to do this.

    Examples
    --------
    Use `index_humansorted` just like the builtin `sorted`::

        >>> a = ['Apple', 'Banana', 'apple', 'banana']
        >>> index_humansorted(a)
        [2, 0, 3, 1]

    """
    return index_natsorted(seq, key, reverse=reverse, alg=alg | ns.LOCALE)


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
    index_humansorted

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
