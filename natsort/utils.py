# -*- coding: utf-8 -*-
"""
Utilities and definitions for natsort, mostly all used to define
the _natsort_key function.

"""

from __future__ import (print_function, division,
                        unicode_literals, absolute_import)

# Std. lib imports.
import re
from warnings import warn
from os import curdir, pardir
from os.path import split, splitext
from itertools import islice
from locale import localeconv

# Local imports.
from natsort.locale_help import locale_convert, grouper
from natsort.py23compat import py23_str, py23_zip
from natsort.ns_enum import ns, _nsdict

# If the user has fastnumbers installed, they will get great speed
# benefits. If not, we simulate the functions here.
try:
    from fastnumbers import fast_float, fast_int, isreal
except ImportError:
    from natsort.fake_fastnumbers import fast_float, fast_int, isreal

# If the user has pathlib installed, the ns.PATH option will convert
# Path objects to str before sorting.
try:
    from pathlib import PurePath  # PurePath is the base object for Paths.
except ImportError:
    PurePath = object  # To avoid NameErrors.
    has_pathlib = False
else:
    has_pathlib = True

# Group algorithm types for easy extraction
_NUMBER_ALGORITHMS = ns.FLOAT | ns.INT | ns.UNSIGNED | ns.NOEXP
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
    # Convert a pathlib PurePath object to a string.
    if has_pathlib and isinstance(s, PurePath):
        path_location = str(s)
    else:
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
                val = val.swapcase()
            if alg & _nsdict['IGNORECASE']:
                val = val.lower()
            return tuple(_input_parser(val,
                                       regex,
                                       num_function,
                                       alg & _nsdict['TYPESAFE'],
                                       use_locale,
                                       alg & _nsdict['GROUPLETTERS']))
        except (TypeError, AttributeError):
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
