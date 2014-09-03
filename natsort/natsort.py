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
from locale import localeconv

# If the user has fastnumbers installed, they will get great speed
# benefits.  If not, we simulate the functions here.
try:
    from fastnumbers import fast_float, fast_int, isreal
except ImportError:
    from .fake_fastnumbers import fast_float, fast_int, isreal
from .locale_help import locale_convert, grouper, lowercase, swapcase
from .py23compat import u_format, py23_str, py23_zip

# Make sure the doctest works for either python2 or python3
__doc__ = u_format(__doc__)


class ns(object):
    """
    Enum to control the `natsort` algorithm.

    This class acts like an enum to control the `natsort` algorithm. The
    user may select several options simultaneously by or'ing the options
    together.  For example, to choose ``ns.INT``, `ns.PATH``, and
    ``ns.LOCALE``, you could do ``ns.INT | ns.LOCALE | ns.PATH``.

    Each option has a shortened 1- or 2-letter form.

    .. warning:: On some systems, the underlying C library that
                 Python's locale module uses is broken. On these
                 systems it is recommended that you install
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_
                 if you wish to use `LOCALE`.
                 Please validate that `LOCALE` works as
                 expected on your target system, and if not you
                 should add
                 `PyICU <https://pypi.python.org/pypi/PyICU>`_
                 as a dependency.

    Attributes
    ----------
    FLOAT, F
        The default - parse numbers as floats.
    INT, I
        Tell `natsort` to parse numbers as ints.
    UNSIGNED, U
        Tell `natsort` to ignore any sign (i.e. "-" or "+") to the
        immediate left of a number.  It is the same as setting the old
        `signed` option to `False`.
    VERSION, V
        This is a shortcut for ``ns.INT | ns.UNSIGNED``, which is useful
        when attempting to sort version numbers.  It is the same as
        setting the old `number_type` option to `None`.
    DIGIT, D
        Same as `VERSION` above.
    NOEXP, N
        Tell `natsort` to not search for exponents as part of the number.
        For example, with `NOEXP` the number "5.6E5" would be interpreted
        as `5.6`, `"E"`, and `5`.  It is the same as setting the old `exp`
        option to `False`.
    PATH, P
        Tell `natsort` to interpret strings as filesystem paths, so they
        will be split according to the filesystem separator
        (i.e. ‘/’ on UNIX, ‘\’ on Windows), as well as splitting on the
        file extension, if any. Without this, lists of file paths like
        ``['Folder/', 'Folder (1)/', 'Folder (10)/']`` will not be sorted
        properly; 'Folder/' will be placed at the end, not at the front.
        It is the same as setting the old `as_path` option to `True`.
    LOCALE, L
        Tell `natsort` to be locale-aware when sorting strings (everything
        that was not converted to a number).  Your sorting results will vary
        depending on your current locale. Generally, the `GROUPLETTERS`
        option is needed with `LOCALE` because the `locale` library
        groups the letters in the same manner (although you may still
        need `GROUPLETTERS` if there are numbers in your strings).
    IGNORECASE, IC
        Tell `natsort` to ignore case when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['apple', 'Apple', 'Banana', 'banana']``.
    LOWERCASEFIRST, LF
        Tell `natsort` to put lowercase letters before uppercase letters
        when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['apple', 'banana', 'Apple', 'Banana']`` (the default order
        would be ``['Apple', 'Banana', 'apple', 'banana']`` which is
        the order from a purely ordinal sort).
        Useless when used with `IGNORECASE`.
    GROUPLETTERS, G
        Tell `natsort` to group lowercase and uppercase letters together
        when sorting.  For example,
        ``['Banana', 'apple', 'banana', 'Apple']`` would be sorted as
        ``['Apple', 'apple', 'Banana', 'banana']``.
        Useless when used with `IGNORECASE`; use with `LOWERCASEFIRST`
        to reverse the order of upper and lower case.
    TYPESAFE, T
        Try hard to avoid "unorderable types" error on Python 3. It
        is the same as setting the old `py3_safe` option to `True`.

    Notes
    -----
    If using `LOCALE`, you may find that if you do not explicitly set
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

    """
    pass


# Sort algorithm "enum" values.
_nsdict = {'FLOAT': 0,           'F': 0,
           'INT': 1,             'I': 1,
           'UNSIGNED': 2,        'U': 2,
           'VERSION': 3,         'V': 3,  # Shortcut for INT | UNSIGNED
           'DIGIT': 3,           'D': 3,  # Shortcut for INT | UNSIGNED
           'NOEXP': 4,           'N': 4,
           'PATH': 8,            'P': 8,
           'LOCALE': 16,         'L': 16,
           'IGNORECASE': 32,     'IC': 32,
           'LOWERCASEFIRST': 64, 'LF': 64,
           'GROUPLETTERS': 128,  'G': 128,
           'TYPESAFE': 1024,     'T': 1024,
           }
# Populate the ns class with the _nsdict values.
for x, y in _nsdict.items():
    setattr(ns, x, y)

# Group algorithm types for easy extraction
_NUMBER_ALGORITHMS = ns.FLOAT | ns.INT | ns.UNSIGNED | ns.NOEXP
_CASE_ALGORITHMS = ns.IGNORECASE | ns.LOWERCASEFIRST | ns.GROUPLETTERS
_ALL_BUT_PATH = (ns.F | ns.I | ns.U | ns.N | ns.L |
                 ns.IC | ns.LF | ns.G | ns.TYPESAFE)

# The regex that locates floats
_float_sign_exp_re = re.compile(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', re.U)
_float_nosign_exp_re = re.compile(r'(\d*\.?\d+(?:[eE][-+]?\d+)?)', re.U)
_float_sign_noexp_re = re.compile(r'([-+]?\d*\.?\d+)', re.U)
_float_nosign_noexp_re = re.compile(r'(\d*\.?\d+)', re.U)
_float_sign_exp_re_c = re.compile(r'([-+]?\d*[.,]?\d+(?:[eE][-+]?\d+)?)', re.U)
_float_nosign_exp_re_c = re.compile(r'(\d*[.,]?\d+(?:[eE][-+]?\d+)?)', re.U)
_float_sign_noexp_re_c = re.compile(r'([-+]?\d*[.,]?\d+)', re.U)
_float_nosign_noexp_re_c = re.compile(r'(\d*[.,]?\d+)', re.U)

# Integer regexes
_int_nosign_re = re.compile(r'(\d+)', re.U)
_int_sign_re = re.compile(r'([-+]?\d+)', re.U)

# This dict will help select the correct regex and number conversion function.
_regex_and_num_function_chooser = {
    (ns.F, '.'):               (_float_sign_exp_re,     fast_float),
    (ns.F | ns.N, '.'):        (_float_sign_noexp_re,   fast_float),
    (ns.F | ns.U, '.'):        (_float_nosign_exp_re,   fast_float),
    (ns.F | ns.U | ns.N, '.'): (_float_nosign_noexp_re, fast_float),
    (ns.I, '.'):               (_int_sign_re,   fast_int),
    (ns.I | ns.N, '.'):        (_int_sign_re,   fast_int),
    (ns.I | ns.U, '.'):        (_int_nosign_re, fast_int),
    (ns.I | ns.U | ns.N, '.'): (_int_nosign_re, fast_int),
    (ns.F, ','):               (_float_sign_exp_re_c,     fast_float),
    (ns.F | ns.N, ','):        (_float_sign_noexp_re_c,   fast_float),
    (ns.F | ns.U, ','):        (_float_nosign_exp_re_c,   fast_float),
    (ns.F | ns.U | ns.N, ','): (_float_nosign_noexp_re_c, fast_float),
    (ns.I, ','):               (_int_sign_re,   fast_int),
    (ns.I | ns.N, ','):        (_int_sign_re,   fast_int),
    (ns.I | ns.U, ','):        (_int_nosign_re, fast_int),
    (ns.I | ns.U | ns.N, ','): (_int_nosign_re, fast_int),
}


def _args_to_enum(number_type, signed, exp, as_path, py3_safe):
    """A function to convert input booleans to an enum-type argument."""
    alg = 0
    if number_type is not float:
        msg = "The 'number_type' argument is depreciated as of 3.5.0, "
        msg += "please use 'alg=ns.FLOAT', 'alg=ns.INT', or 'alg=ns.VERSION'"
        warn(msg, DeprecationWarning)
        alg |= (_nsdict['INT'] * bool(number_type in (int, None)))
        alg |= (_nsdict['UNSIGNED'] * (number_type is None))
    if signed is not None:
        msg = "The 'signed' argument is depreciated as of 3.5.0, "
        msg += "please use 'alg=ns.UNSIGNED'."
        warn(msg, DeprecationWarning)
        alg |= (_nsdict['UNSIGNED'] * (not signed))
    if exp is not None:
        msg = "The 'exp' argument is depreciated as of 3.5.0, "
        msg += "please use 'alg=ns.NOEXP'."
        warn(msg, DeprecationWarning)
        alg |= (_nsdict['NOEXP'] * (not exp))
    if as_path is not None:
        msg = "The 'as_path' argument is depreciated as of 3.5.0, "
        msg += "please use 'alg=ns.PATH'."
        warn(msg, DeprecationWarning)
        alg |= (_nsdict['PATH'] * as_path)
    if py3_safe is not None:
        msg = "The 'py3_safe' argument is depreciated as of 3.5.0, "
        msg += "please use 'alg=ns.TYPESAFE'."
        warn(msg, DeprecationWarning)
        alg |= (_nsdict['TYPESAFE'] * py3_safe)
    return alg


def _input_parser(s, regex, numconv, py3_safe, use_locale, group_letters):
    """Helper to parse the string input into numbers and strings."""

    # Split the input string by numbers.
    # If the input is not a string, TypeError is raised.
    s = regex.split(s)

    # Now convert the numbers to numbers, and leave strings as strings.
    # Take into account locale if needed, and group letters if needed.
    # Remove empty strings from the list.
    if use_locale:
        s = [locale_convert(x, numconv, group_letters) for x in s if x]
    elif group_letters:
        s = [grouper(x, numconv) for x in s if x]
    else:
        s = [numconv(x) for x in s if x]

    # If the list begins with a number, lead with an empty string.
    # This is used to get around the "unorderable types" issue.
    if not s:  # Return empty tuple for empty results.
        return ()
    elif isreal(s[0]):
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


def _natsort_key(val, key, alg):
    """\
    Key to sort strings and numbers naturally.

    It works by separating out the numbers from the strings. This function for
    internal use only. See the natsort_keygen documentation for details of each
    parameter.

    Parameters
    ----------
    val : {str, unicode}
    key : callable
    alg : ns enum

    Returns
    -------
    out : tuple
        The modified value with numbers extracted.

    """

    # Convert the arguments to the proper input tuple
    try:
        use_locale = alg & _nsdict['LOCALE']
        inp_options = (alg & _NUMBER_ALGORITHMS,
                       localeconv()['decimal_point'] if use_locale else '.')
    except TypeError:
        msg = "_natsort_key: 'alg' argument must be from the enum 'ns'"
        raise ValueError(msg+', got {0}'.format(py23_str(alg)))

    # Get the proper regex and conversion function.
    try:
        regex, num_function = _regex_and_num_function_chooser[inp_options]
    except KeyError:  # pragma: no cover
        if inp_options[1] not in ('.', ','):  # pragma: no cover
            raise ValueError("_natsort_key: currently natsort only supports "
                             "the decimal separators '.' and ','. "
                             "Please file a bug report.")
        else:
            raise
    else:
        # Apply key if needed.
        if key is not None:
            val = key(val)

        # If this is a path, convert it.
        # An AttrubuteError is raised if not a string.
        split_as_path = False
        if alg & _nsdict['PATH']:
            try:
                val = _path_splitter(val)
            except AttributeError:
                pass
            else:
                # Record that this string was split as a path so that
                # we don't set PATH in the recursive call.
                split_as_path = True

        # Assume the input are strings, which is the most common case.
        # Apply the string modification if needed.
        try:
            if alg & _nsdict['LOWERCASEFIRST']:
                val = swapcase(val)
            if alg & _nsdict['IGNORECASE']:
                val = lowercase(val)
            return tuple(_input_parser(val,
                                       regex,
                                       num_function,
                                       alg & _nsdict['TYPESAFE'],
                                       use_locale,
                                       alg & _nsdict['GROUPLETTERS']))
        except TypeError:
            # If not strings, assume it is an iterable that must
            # be parsed recursively. Do not apply the key recursively.
            # If this string was split as a path, turn off 'PATH'.
            try:
                was_path = alg & _nsdict['PATH']
                newalg = alg & _ALL_BUT_PATH
                newalg |= (was_path * (not split_as_path))
                return tuple([_natsort_key(x, None, newalg) for x in val])
            # If there is still an error, it must be a number.
            # Return as-is, with a leading empty string.
            except TypeError:
                return (('', val,),) if alg & _nsdict['PATH'] else ('', val,)


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
    versorted : A wrapper for ``natsorted(seq, number_type=None)``.
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
                                             alg=alg | _nsdict['TYPESAFE']))
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
