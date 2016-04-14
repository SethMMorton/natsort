# -*- coding: utf-8 -*-
"""
Utilities and definitions for natsort, mostly all used to define
the _natsort_key function.
"""
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# Std. lib imports.
import sys
import re
from warnings import warn
from os import curdir as os_curdir, pardir as os_pardir
from os.path import split as path_split, splitext as path_splitext
from itertools import islice
from locale import localeconv
from collections import deque
from functools import partial
from operator import methodcaller

# Local imports.
from natsort.ns_enum import ns
from natsort.unicode_numbers import digits, numeric
from natsort.locale_help import locale_convert, groupletters
from natsort.compat.pathlib import PurePath, has_pathlib
from natsort.compat.py23 import (
    py23_str,
    py23_zip,
    py23_map,
    py23_filter,
    PY_VERSION,
)
from natsort.compat.locale import (
    dumb_sort,
    use_pyicu,
    null_string,
)
from natsort.compat.fastnumbers import (
    fast_float,
    fast_int,
    isint,
    isfloat,
)
if sys.version[0] == '3':
    long = int

# The regex that locates floats - include Unicode numerals.
_exp = r'(?:[eE][-+]?[0-9]+)?'
_num = r'(?:[0-9]+\.?[0-9]*|\.[0-9]+)'
_num_c = r'(?:[0-9]+[.,]?[0-9]*|[.,][0-9]+)'
_float_sign_exp_re = r'([-+]?{0}{1}|[{2}])'
_float_sign_exp_re = _float_sign_exp_re.format(_num, _exp, numeric)
_float_sign_exp_re = re.compile(_float_sign_exp_re, flags=re.U)
_float_nosign_exp_re = r'({0}{1}|[{2}])'
_float_nosign_exp_re = _float_nosign_exp_re.format(_num, _exp, numeric)
_float_nosign_exp_re = re.compile(_float_nosign_exp_re, flags=re.U)
_float_sign_noexp_re = r'([-+]?{0}|[{1}])'
_float_sign_noexp_re = _float_sign_noexp_re.format(_num, numeric)
_float_sign_noexp_re = re.compile(_float_sign_noexp_re, flags=re.U)
_float_nosign_noexp_re = r'({0}|[{1}])'
_float_nosign_noexp_re = _float_nosign_noexp_re.format(_num, numeric)
_float_nosign_noexp_re = re.compile(_float_nosign_noexp_re, flags=re.U)
_float_sign_exp_re_c = r'([-+]?{0}{1}|[{2}])'
_float_sign_exp_re_c = _float_sign_exp_re_c.format(_num_c, _exp, numeric)
_float_sign_exp_re_c = re.compile(_float_sign_exp_re_c, flags=re.U)
_float_nosign_exp_re_c = r'({0}{1}|[{2}])'
_float_nosign_exp_re_c = _float_nosign_exp_re_c.format(_num_c, _exp, numeric)
_float_nosign_exp_re_c = re.compile(_float_nosign_exp_re_c, flags=re.U)
_float_sign_noexp_re_c = r'([-+]?{0}|[{1}])'
_float_sign_noexp_re_c = _float_sign_noexp_re_c.format(_num_c, numeric)
_float_sign_noexp_re_c = re.compile(_float_sign_noexp_re_c, flags=re.U)
_float_nosign_noexp_re_c = r'({0}|[{1}])'
_float_nosign_noexp_re_c = _float_nosign_noexp_re_c.format(_num_c, numeric)
_float_nosign_noexp_re_c = re.compile(_float_nosign_noexp_re_c, flags=re.U)

# Integer regexes - include Unicode digits.
_int_nosign_re = r'([0-9]+|[{0}])'.format(digits)
_int_nosign_re = re.compile(_int_nosign_re, flags=re.U)
_int_sign_re = r'([-+]?[0-9]+|[{0}])'.format(digits)
_int_sign_re = re.compile(_int_sign_re, flags=re.U)

# This dict will help select the correct regex and number conversion function.
_regex_and_num_function_chooser = {
    (ns.F | ns.S, '.'):        (_float_sign_exp_re,     fast_float),
    (ns.F | ns.S | ns.N, '.'): (_float_sign_noexp_re,   fast_float),
    (ns.F | ns.U, '.'):        (_float_nosign_exp_re,   fast_float),
    (ns.F | ns.U | ns.N, '.'): (_float_nosign_noexp_re, fast_float),
    (ns.I | ns.S, '.'):        (_int_sign_re,   fast_int),
    (ns.I | ns.S | ns.N, '.'): (_int_sign_re,   fast_int),
    (ns.I | ns.U, '.'):        (_int_nosign_re, fast_int),
    (ns.I | ns.U | ns.N, '.'): (_int_nosign_re, fast_int),
    (ns.F | ns.S, ','):        (_float_sign_exp_re_c,     fast_float),
    (ns.F | ns.S | ns.N, ','): (_float_sign_noexp_re_c,   fast_float),
    (ns.F | ns.U, ','):        (_float_nosign_exp_re_c,   fast_float),
    (ns.F | ns.U | ns.N, ','): (_float_nosign_noexp_re_c, fast_float),
    (ns.I | ns.S, ','):        (_int_sign_re,   fast_int),
    (ns.I | ns.S | ns.N, ','): (_int_sign_re,   fast_int),
    (ns.I | ns.U, ','):        (_int_nosign_re, fast_int),
    (ns.I | ns.U | ns.N, ','): (_int_nosign_re, fast_int),
}

# Dict to select checker function from converter function
_conv_to_check = {fast_float: isfloat, fast_int: isint}


def _do_decoding(s, encoding):
    """A function to decode a bytes string, or return the object as-is."""
    try:
        return s.decode(encoding)
    except UnicodeError:
        raise
    except (AttributeError, TypeError):
        return s


def _args_to_enum(**kwargs):
    """A function to convert input booleans to an enum-type argument."""
    alg = 0
    keys = ('number_type', 'signed', 'exp', 'as_path', 'py3_safe')
    if any(x not in keys for x in kwargs):
        x = set(kwargs) - set(keys)
        raise TypeError('Invalid argument(s): ' + ', '.join(x))
    if 'number_type' in kwargs and kwargs['number_type'] is not int:
        msg = "The 'number_type' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.FLOAT', 'alg=ns.INT', or 'alg=ns.VERSION'"
        warn(msg, DeprecationWarning)
        alg |= (ns.FLOAT * bool(kwargs['number_type'] is float))
        alg |= (ns.INT * bool(kwargs['number_type'] in (int, None)))
        alg |= (ns.SIGNED * (kwargs['number_type'] not in (float, None)))
    if 'signed' in kwargs and kwargs['signed'] is not None:
        msg = "The 'signed' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.SIGNED'."
        warn(msg, DeprecationWarning)
        alg |= (ns.SIGNED * bool(kwargs['signed']))
    if 'exp' in kwargs and kwargs['exp'] is not None:
        msg = "The 'exp' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.NOEXP'."
        warn(msg, DeprecationWarning)
        alg |= (ns.NOEXP * (not kwargs['exp']))
    if 'as_path' in kwargs and kwargs['as_path'] is not None:
        msg = "The 'as_path' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.PATH'."
        warn(msg, DeprecationWarning)
        alg |= (ns.PATH * kwargs['as_path'])
    return alg


def _chain_functions(functions):
    """Chain a list of single-argument functions together and return"""
    def func(x, _functions=functions):
        output = x
        for f in _functions:
            output = f(output)
        return output
    return func


def _pre_split_function(alg):
    """
    Given a set of natsort algorithms, return the function to operate
    on the pre-split input string according to the user's request.
    """
    lowfirst = alg & ns.LOWERCASEFIRST
    dumb = alg & ns._DUMB
    function_chain = []
    if (dumb and not lowfirst) or (lowfirst and not dumb):
        function_chain.append(methodcaller('swapcase'))
    if alg & ns.IGNORECASE:
        if PY_VERSION >= 3.3:
            function_chain.append(methodcaller('casefold'))
        else:
            function_chain.append(methodcaller('lower'))
    return _chain_functions(function_chain)


def _number_extracter(s, regex, numconv, use_locale, group_letters):
    """Helper to separate the string input into numbers and strings."""

    # Split the input string by numbers, dropping empty strings.
    # If the input is not a string, TypeError is raised.
    s = py23_filter(None, regex.split(s))

    # Now convert the numbers to numbers, and leave strings as strings.
    # Take into account locale if needed, and group letters if needed.
    # Remove empty strings from the list. Insert empty strings between
    # adjascent numbers, or at the beginning of the iterable if it is
    # a number.
    if use_locale and group_letters:
        func = partial(numconv, key=partial(locale_convert, key=groupletters))
    elif use_locale:
        func = partial(numconv, key=locale_convert)
    elif group_letters:
        func = partial(numconv, key=groupletters)
    else:
        func = numconv
    return list(_sep_inserter(py23_map(func, s),
                              null_string if use_locale else ''))


def _path_splitter(s, _d_match=re.compile(r'\.\d').match):
    """Split a string into its path components. Assumes a string is a path."""
    # If a PathLib Object, use it's functionality to perform the split.
    if has_pathlib and isinstance(s, PurePath):
        path_parts = deque(s.parts)
    else:
        path_parts = deque()
        p_appendleft = path_parts.appendleft
        # Continue splitting the path from the back until we have reached
        # '..' or '.', or until there is nothing left to split.
        path_location = s
        while path_location != os_curdir and path_location != os_pardir:
            parent_path = path_location
            path_location, child_path = path_split(parent_path)
            if path_location == parent_path:
                break
            p_appendleft(child_path)

        # This last append is the base path.
        # Only append if the string is non-empty.
        if path_location:
            p_appendleft(path_location)

    # Now, split off the file extensions using a similar method to above.
    # Continue splitting off file extensions until we reach a decimal number
    # or there are no more extensions.
    # We are not using built-in functionality of PathLib here because of
    # the recursive splitting up to a decimal.
    base = path_parts.pop()
    base_parts = deque()
    b_appendleft = base_parts.appendleft
    while True:
        front = base
        base, ext = path_splitext(front)
        if _d_match(ext) or not ext:
            # Reset base to before the split if the split is invalid.
            base = front
            break
        b_appendleft(ext)
    b_appendleft(base)

    # Return the split parent paths and then the split basename.
    return tuple(path_parts + base_parts)


def _sep_inserter(iterable, sep):
    """Insert '' between numbers."""

    # Get the first element. If StopIteration is raised, that's OK.
    types = (int, float, long)
    first = next(iterable)
    if type(first) in types:
        yield sep
    yield first

    # Now, check if pair of elements are both numbers. If so, add ''.
    second = next(iterable)
    if type(first) in types and type(second) in types:
        yield sep
    yield second

    # Now repeat in a loop.
    for x in iterable:
        first, second = second, x
        if type(first) in types and type(second) in types:
            yield sep
        yield second


def _fix_nan(ret, alg):
    """Detect an NaN and replace or raise a ValueError."""
    t = []
    for r in ret:
        if r != r:
            if alg & ns.NANLAST:
                t.append(float('+inf'))
            else:
                t.append(float('-inf'))
        else:
            t.append(r)
    return tuple(t)


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
        use_locale = alg & ns.LOCALE
        inp_options = (alg & ns._NUMERIC_ONLY,
                       localeconv()['decimal_point'] if use_locale else '.')
    except TypeError:
        msg = "_natsort_key: 'alg' argument must be from the enum 'ns'"
        raise ValueError(msg+', got {0}'.format(py23_str(alg)))

    # Get the proper regex and conversion function.
    try:
        regex, num_function = _regex_and_num_function_chooser[inp_options]
    except KeyError:  # pragma: no cover
        if inp_options[1] not in ('.', ','):
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
        if alg & ns.PATH:
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
        orig_val = val
        try:
            if use_locale and dumb_sort():
                alg |= ns._DUMB
            lowfirst = alg & ns.LOWERCASEFIRST
            dumb = alg & ns._DUMB
            val = _pre_split_function(alg)(val)
            gl = alg & ns.GROUPLETTERS
            ret = tuple(_number_extracter(val,
                                          regex,
                                          num_function,
                                          use_locale,
                                          gl or (use_locale and dumb)))
            # Handle NaN.
            if any(x != x for x in ret):
                ret = _fix_nan(ret, alg)
            # For UNGROUPLETTERS, so the high level grouping can occur
            # based on the first letter of the string.
            # Do no locale transformation of the characters.
            if use_locale and alg & ns.UNGROUPLETTERS:
                if not ret:
                    return (ret, ret)
                elif ret[0] == null_string:
                    return ((b'' if use_pyicu else '',), ret)
                elif dumb:  # pragma: no cover
                    if lowfirst:
                        return ((orig_val[0].swapcase(),), ret)
                    else:
                        return ((orig_val[0],), ret)
                else:
                    return ((val[0],), ret)
            else:
                return ret
        except (TypeError, AttributeError):
            # Check if it is a bytes type, and if so return as a
            # one element tuple.
            if type(val) in (bytes,):
                return (val.lower(),) if alg & ns.IGNORECASE else (val,)
            # If not strings, assume it is an iterable that must
            # be parsed recursively. Do not apply the key recursively.
            # If this string was split as a path, turn off 'PATH'.
            try:
                was_path = alg & ns.PATH
                newalg = alg & ns._ALL_BUT_PATH
                newalg |= (was_path * (not split_as_path))
                return tuple([_natsort_key(x, None, newalg) for x in val])
            # If there is still an error, it must be a number.
            # Return as-is, with a leading empty string.
            except TypeError:
                n = null_string if use_locale else ''
                if val != val:
                    val = _fix_nan([val], alg)[0]
                return ((n, val,),) if alg & ns.PATH else (n, val,)
