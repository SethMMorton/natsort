"""
Replication of fastnumbers functionality.

Used when the fastnumbers module is not installed.
"""

from __future__ import annotations

import unicodedata
from decimal import Decimal, InvalidOperation
from typing import Callable, Union

from natsort.unicode_numbers import decimal_chars

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

StrOrFloat = Union[str, float, Decimal]
StrOrInt = Union[str, int]


def _widen_if_overflowed(x: str, ret: float) -> StrOrFloat:
    """
    Widen a float that overflowed to +/-inf back into something orderable.

    float() silently rounds a finite number with too large a magnitude to
    +/-inf instead of raising, so two different numbers like "1e400" and
    "1e500" would otherwise both come out as inf and compare equal, losing
    their relative order. Decimal has a much larger exponent range, so use
    it to keep such values distinguishable. A literal "inf"/"nan" spelling
    is left alone as a plain float, since it isn't the result of an overflow.
    """
    if ret not in (float("inf"), float("-inf")):
        return ret
    if x.strip().lstrip("+-")[:3].lower() in ("inf", "nan"):
        return ret
    try:
        return Decimal(x)
    except InvalidOperation:  # pragma: no cover
        return ret


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
            return nan if ret != ret else _widen_if_overflowed(x, ret)
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
            try:
                return _uni(x, key(x)) if len(x) == 1 else key(x)
            except TypeError:  # pragma: no cover
                return key(x)
    else:
        try:
            return _uni(x, key(x)) if len(x) == 1 else key(x)
        except TypeError:  # pragma: no cover
            return key(x)
