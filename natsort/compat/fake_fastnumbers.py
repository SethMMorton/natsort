"""
Replication of fastnumbers functionality.

Used when the fastnumbers module is not installed.
"""

from __future__ import annotations

import sys
import unicodedata
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable, Union

from natsort.unicode_numbers import decimal_chars

if TYPE_CHECKING:
    from collections.abc import Iterator

# Python 3.11 added a guard rail that makes int() (and str(int)) raise
# ValueError for digit runs longer than sys.get_int_max_str_digits(),
# to keep a hostile huge numeric string from stalling a program. The
# fastnumbers C extension that this module stands in for has no such
# limit, so without accounting for it here, a natsort call would behave
# differently for an oversized numeric token depending on whether that
# optional dependency happens to be installed: a plain string (that no
# longer sorts consistently with the other, ordinarily-sized numbers
# next to it) versus an int.
_HAS_INT_MAX_STR_DIGITS = hasattr(sys, "set_int_max_str_digits")


@contextmanager
def _int_max_str_digits_disabled() -> Iterator[None]:
    """Temporarily lift the int() digit-count guard rail, if it exists."""
    if not _HAS_INT_MAX_STR_DIGITS:
        yield
        return
    previous_limit = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    try:
        yield
    finally:
        sys.set_int_max_str_digits(previous_limit)


_NAN_INF = [
    "INF",
    "INf",
    "Inf",
    "inF",
    "iNF",
    "InF",
    "inf",
    "iNf",
    "NAN",
    "nan",
    "NaN",
    "nAn",
    "naN",
    "NAn",
    "nAN",
    "Nan",
]
_NAN_INF.extend(["+" + x[:2] for x in _NAN_INF] + ["-" + x[:2] for x in _NAN_INF])
NAN_INF = frozenset(_NAN_INF)
ASCII_NUMS = "0123456789+-"
POTENTIAL_FIRST_CHAR = frozenset(decimal_chars + list(ASCII_NUMS + "."))

StrOrFloat = Union[str, float]
StrOrInt = Union[str, int]


def fast_float(
    x: str,
    key: Callable[[str], str] = lambda x: x,
    nan: float = float("inf"),
    _uni: Callable[[str, StrOrFloat], StrOrFloat] = unicodedata.numeric,
    _nan_inf: frozenset[str] = NAN_INF,
    _first_char: frozenset[str] = POTENTIAL_FIRST_CHAR,
) -> StrOrFloat:
    """
    Convert a string to a float quickly, return input as-is if not possible.

    We don't need to accept all input that the real fast_int accepts because
    natsort is controlling what is passed to this function.

    Parameters
    ----------
    x : str
        String to attempt to convert to a float.
    key : callable
        Single-argument function to apply to *x* if conversion fails.
    nan : float
        Value to return instead of NaN if NaN would be returned.

    Returns
    -------
    *str* or *float*

    """
    if x[:1] in _first_char or x.lstrip()[:3] in _nan_inf:
        try:
            ret = float(x)
        except ValueError:
            try:
                return _uni(x, key(x)) if len(x) == 1 else key(x)
            except TypeError:  # pragma: no cover
                return key(x)
        else:
            return nan if ret != ret else ret
    else:
        try:
            return _uni(x, key(x)) if len(x) == 1 else key(x)
        except TypeError:  # pragma: no cover
            return key(x)


def fast_int(
    x: str,
    key: Callable[[str], str] = lambda x: x,
    _uni: Callable[[str, StrOrInt], StrOrInt] = unicodedata.digit,
    _first_char: frozenset[str] = POTENTIAL_FIRST_CHAR,
) -> StrOrInt:
    """
    Convert a string to a int quickly, return input as-is if not possible.

    We don't need to accept all input that the real fast_int accepts because
    natsort is controlling what is passed to this function.

    Parameters
    ----------
    x : str
        String to attempt to convert to an int.
    key : callable
        Single-argument function to apply to *x* if conversion fails.

    Returns
    -------
    *str* or *int*

    """
    if x[:1] in _first_char:
        try:
            return int(x)
        except ValueError:
            unsigned = x[1:] if x[:1] in "+-" else x
            if unsigned.isdecimal():
                # This wasn't "not an int"; it was int() refusing a
                # too-long-but-otherwise-perfectly-valid digit run
                # (see _int_max_str_digits_disabled above). Convert it
                # anyway so it keeps sorting as a number.
                with _int_max_str_digits_disabled():
                    return int(x)
            try:
                return _uni(x, key(x)) if len(x) == 1 else key(x)
            except TypeError:  # pragma: no cover
                return key(x)
    else:
        try:
            return _uni(x, key(x)) if len(x) == 1 else key(x)
        except TypeError:  # pragma: no cover
            return key(x)
