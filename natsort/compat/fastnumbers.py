"""
Compatibility interface for fastnumbers.

Provides a uniform interface to fastnumbers or the fallbacks.
"""

from __future__ import annotations

import re
from decimal import Decimal
from typing import TYPE_CHECKING, Callable, Union

from natsort.compat.fake_fastnumbers import widen_if_overflowed
from natsort.compat.locale import StrOrBytes

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

# str/bytes can come back out when on_fail is given and the input could not
# be converted (e.g. groupletters or a locale-aware strxfrm, either of
# which may return bytes). Decimal can come back out when a magnitude was
# too large for a float and got widened to keep its relative order.
StrOrFloat = Union[StrOrBytes, float, Decimal]
StrOrInt = Union[str, int]

__all__ = ["try_float", "try_int"]


def is_supported_fastnumbers(
    fastnumbers_version: str,
    minimum: tuple[int, int, int] = (2, 0, 0),
) -> bool:
    match = re.match(
        r"^(\d+)\.(\d+)(\.(\d+))?([ab](\d+))?$",
        fastnumbers_version,
        flags=re.ASCII,
    )

    if not match:
        msg = f"Invalid fastnumbers version number '{fastnumbers_version}'"
        raise ValueError(msg)

    (major, minor, patch) = match.group(1, 2, 4)

    return (int(major), int(minor), int(patch)) >= minimum


def ensure_minimum_fastnumbers(fastnumbers_version: str) -> None:
    if not is_supported_fastnumbers(fastnumbers_version):
        msg = "fastnumbers package version not modern enough"
        raise ImportError(msg)


# If the user has fastnumbers installed, they will get great speed
# benefits. If not, we use the simulated functions that come with natsort.
#
# Note that whichever float-conversion primitive we end up with here
# (fast_float, or the newer mapping-capable try_float) is only used as
# the *raw* building block for this module's own try_float below - none
# of them are re-exported directly. That raw primitive rounds a finite
# number with too large a magnitude to +/-inf, same as the float()
# builtin, so on its own it can't tell two overflowing values like
# "1e400" and "1e500" apart. This module's try_float always widens such
# results to Decimal afterwards, so that behavior is consistent no matter
# which backend produced the raw float.
try:
    # noinspection PyPackageRequirements
    from fastnumbers import __version__ as fn_ver
    from fastnumbers import fast_float, fast_int

    # Require >= version 2.0.0.
    ensure_minimum_fastnumbers(fn_ver)

    # For versions of fastnumbers with mapping capability, use that
    if is_supported_fastnumbers(fn_ver, (5, 0, 0)):
        del fast_float, fast_int
        from fastnumbers import try_float as _raw_try_float_map
        from fastnumbers import try_int
except ImportError:
    from natsort.compat.fake_fastnumbers import (  # type: ignore[no-redef]
        fast_float,
        fast_int,
    )

if "try_int" not in globals():

    def try_int(  # type: ignore[no-redef]
        x: Iterable[str],
        *,
        map: bool,
        on_fail: Callable[[str], str] = lambda x: x,
    ) -> Iterator[StrOrInt]:
        """Attempt to convert a string to an int."""
        assert map is True  # noqa: S101
        return (fast_int(y, key=on_fail) for y in x)


def _raw_try_float(
    x: list[str],
    *,
    nan: float,
    on_fail: Callable[[str], StrOrBytes],
) -> Iterable[StrOrFloat]:
    """Convert strings to floats using whichever backend is available."""
    if "_raw_try_float_map" in globals():
        return _raw_try_float_map(x, nan=nan, on_fail=on_fail, map=True)
    return (fast_float(y, nan=nan, key=on_fail) for y in x)


def try_float(
    x: Iterable[str],
    *,
    map: bool,
    nan: float = float("inf"),
    on_fail: Callable[[str], StrOrBytes] = lambda x: x,
) -> Iterator[StrOrFloat]:
    """Attempt to convert a string to a float."""
    assert map is True  # noqa: S101
    values = list(x)
    raw_results = _raw_try_float(values, nan=nan, on_fail=on_fail)
    return (
        widen_if_overflowed(orig, ret) if isinstance(ret, float) else ret
        for orig, ret in zip(values, raw_results)
    )
