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
import re
from math import isnan
from warnings import warn
from os import curdir, pardir
from os.path import split, splitext
from itertools import islice
from locale import localeconv

# Local imports.
from natsort.ns_enum import ns, _ns
from natsort.unicode_numbers import digits, numeric
from natsort.locale_help import locale_convert, grouper
from natsort.compat.pathlib import PurePath, has_pathlib
from natsort.compat.py23 import (
    py23_str,
    py23_zip,
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

# Group algorithm types for easy extraction
_NUMBER_ALGORITHMS = ns.FLOAT | ns.INT | ns.UNSIGNED | ns.SIGNED | ns.NOEXP
_ALL_BUT_PATH = (ns.F | ns.I | ns.U | ns.S | ns.N | ns.L |
                 ns.IC | ns.LF | ns.G | ns.UG | ns.TYPESAFE)

# The regex that locates floats - include Unicode numerals.
_float_sign_exp_re = r'([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?|[{0}])'
_float_sign_exp_re = _float_sign_exp_re.format(numeric)
_float_sign_exp_re = re.compile(_float_sign_exp_re, flags=re.U)
_float_nosign_exp_re = r'([0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?|[{0}])'
_float_nosign_exp_re = _float_nosign_exp_re.format(numeric)
_float_nosign_exp_re = re.compile(_float_nosign_exp_re, flags=re.U)
_float_sign_noexp_re = r'([-+]?[0-9]*\.?[0-9]+|[{0}])'
_float_sign_noexp_re = _float_sign_noexp_re.format(numeric)
_float_sign_noexp_re = re.compile(_float_sign_noexp_re, flags=re.U)
_float_nosign_noexp_re = r'([0-9]*\.?[0-9]+|[{0}])'
_float_nosign_noexp_re = _float_nosign_noexp_re.format(numeric)
_float_nosign_noexp_re = re.compile(_float_nosign_noexp_re, flags=re.U)
_float_sign_exp_re_c = r'([-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?)|[{0}]'
_float_sign_exp_re_c = _float_sign_exp_re_c.format(numeric)
_float_sign_exp_re_c = re.compile(_float_sign_exp_re_c, flags=re.U)
_float_nosign_exp_re_c = r'([0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?|[{0}])'
_float_nosign_exp_re_c = _float_nosign_exp_re_c.format(numeric)
_float_nosign_exp_re_c = re.compile(_float_nosign_exp_re_c, flags=re.U)
_float_sign_noexp_re_c = r'([-+]?[0-9]*[.,]?[0-9]+|[{0}])'
_float_sign_noexp_re_c = _float_sign_noexp_re_c.format(numeric)
_float_sign_noexp_re_c = re.compile(_float_sign_noexp_re_c, flags=re.U)
_float_nosign_noexp_re_c = r'([0-9]*[.,]?[0-9]+|[{0}])'
_float_nosign_noexp_re_c = _float_nosign_noexp_re_c.format(numeric)
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
        alg |= (_ns['FLOAT'] * bool(kwargs['number_type'] is float))
        alg |= (_ns['INT'] * bool(kwargs['number_type'] in (int, None)))
        alg |= (_ns['SIGNED'] * (kwargs['number_type'] not in (float, None)))
    if 'signed' in kwargs and kwargs['signed'] is not None:
        msg = "The 'signed' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.SIGNED'."
        warn(msg, DeprecationWarning)
        alg |= (_ns['SIGNED'] * bool(kwargs['signed']))
    if 'exp' in kwargs and kwargs['exp'] is not None:
        msg = "The 'exp' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.NOEXP'."
        warn(msg, DeprecationWarning)
        alg |= (_ns['NOEXP'] * (not kwargs['exp']))
    if 'as_path' in kwargs and kwargs['as_path'] is not None:
        msg = "The 'as_path' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.PATH'."
        warn(msg, DeprecationWarning)
        alg |= (_ns['PATH'] * kwargs['as_path'])
    if 'py3_safe' in kwargs and kwargs['py3_safe'] is not None:
        msg = "The 'py3_safe' argument is deprecated as of 3.5.0, "
        msg += "please use 'alg=ns.TYPESAFE'."
        warn(msg, DeprecationWarning)
        alg |= (_ns['TYPESAFE'] * kwargs['py3_safe'])
    return alg


def _number_extracter(s, regex, numconv, py3_safe, use_locale, group_letters):
    """Helper to separate the string input into numbers and strings."""
    conv_check = (numconv, _conv_to_check[numconv])

    # Split the input string by numbers.
    # If the input is not a string, TypeError is raised.
    s = regex.split(s)

    # Now convert the numbers to numbers, and leave strings as strings.
    # Take into account locale if needed, and group letters if needed.
    # Remove empty strings from the list.
    if use_locale:
        s = [locale_convert(x, conv_check, group_letters) for x in s if x]
    elif group_letters:
        s = [grouper(x, conv_check) for x in s if x]
    else:
        s = [numconv(x) for x in s if x]

    # If the list begins with a number, lead with an empty string.
    # This is used to get around the "unorderable types" issue.
    if not s:  # Return empty list for empty results.
        return []
    elif conv_check[1](s[0], num_only=True):
        s = [null_string if use_locale else ''] + s

    # The _py3_safe function inserts "" between numbers in the list,
    # and is used to get around "unorderable types" in complex cases.
    # It is a separate function that needs to be requested specifically
    # because it is expensive to call.
    return _py3_safe(s, use_locale, conv_check[1]) if py3_safe else s


def _path_splitter(s, _d_match=re.compile(r'\.\d').match):
    """Split a string into its path components. Assumes a string is a path."""
    path_parts = []
    p_append = path_parts.append
    # Convert a pathlib PurePath object to a string.
    if has_pathlib and isinstance(s, PurePath):
        path_location = str(s)
    else:  # pragma: no cover
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


def _py3_safe(parsed_list, use_locale, check):
    """Insert '' between two numbers."""
    length = len(parsed_list)
    if length < 2:
        return parsed_list
    else:
        new_list = [parsed_list[0]]
        nl_append = new_list.append
        for before, after in py23_zip(islice(parsed_list, 0, length-1),
                                      islice(parsed_list, 1, None)):
            if check(before, num_only=True) and check(after, num_only=True):
                nl_append(null_string if use_locale else '')
            nl_append(after)
        return new_list


def _fix_nan(ret, alg):
    """Detect an NaN and replace or raise a ValueError."""
    t = []
    for r in ret:
        if isfloat(r, num_only=True) and isnan(r):
            if alg & _ns['NANLAST']:
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
        use_locale = alg & _ns['LOCALE']
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
        if alg & _ns['PATH']:
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
            lowfirst = alg & _ns['LOWERCASEFIRST']
            dumb = dumb_sort() if use_locale else False
            if use_locale and dumb and not lowfirst:  # pragma: no cover
                val = val.swapcase()  # Compensate for bad locale lib.
            elif lowfirst and not (use_locale and dumb):
                val = val.swapcase()
            if alg & _ns['IGNORECASE']:
                val = val.casefold() if PY_VERSION >= 3.3 else val.lower()
            gl = alg & _ns['GROUPLETTERS']
            ret = tuple(_number_extracter(val,
                                          regex,
                                          num_function,
                                          alg & _ns['TYPESAFE'],
                                          use_locale,
                                          gl or (use_locale and dumb)))
            # Handle NaN.
            if any(isfloat(x, num_only=True) and isnan(x) for x in ret):
                ret = _fix_nan(ret, alg)
            # For UNGROUPLETTERS, so the high level grouping can occur
            # based on the first letter of the string.
            # Do no locale transformation of the characters.
            if use_locale and alg & _ns['UNGROUPLETTERS']:
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
                return (val.lower(),) if alg & _ns['IGNORECASE'] else (val,)
            # If not strings, assume it is an iterable that must
            # be parsed recursively. Do not apply the key recursively.
            # If this string was split as a path, turn off 'PATH'.
            try:
                was_path = alg & _ns['PATH']
                newalg = alg & _ALL_BUT_PATH
                newalg |= (was_path * (not split_as_path))
                return tuple([_natsort_key(x, None, newalg) for x in val])
            # If there is still an error, it must be a number.
            # Return as-is, with a leading empty string.
            except TypeError:
                n = null_string if use_locale else ''
                if isfloat(val, num_only=True) and isnan(val):
                    val = _fix_nan([val], alg)[0]
                return ((n, val,),) if alg & _ns['PATH'] else (n, val,)
