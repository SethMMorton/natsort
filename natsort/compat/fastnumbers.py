"""
Compatibility interface for fastnumbers.

Provides a uniform interface to fastnumbers or the fallbacks.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, Union

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

StrOrFloat = Union[str, float]
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
try:
    # noinspection PyPackageRequirements
    from fastnumbers import __version__ as fn_ver
    from fastnumbers import fast_float, fast_int

    # Require >= version 2.0.0.
    ensure_minimum_fastnumbers(fn_ver)

    # For versions of fastnumbers with mapping capability, use that
    if is_supported_fastnumbers(fn_ver, (5, 0, 0)):
        del fast_float, fast_int
        from fastnumbers import try_float, try_int
except ImportError:
    from natsort.compat.fake_fastnumbers import (  # type: ignore[no-redef]
        fast_float,
        fast_int,
    )

# Re-map the old-or-compatibility functions fast_float/fast_int to the
# newer API of try_float/try_int. If we already imported try_float/try_int
# then there is nothing to do.
if "try_float" not in globals():

    def try_float(  # type: ignore[no-redef]
        x: Iterable[str],
        *,
        map: bool,
        nan: float = float("inf"),
        on_fail: Callable[[str], str] = lambda x: x,
    ) -> Iterator[StrOrFloat]:
        """Attempt to convert a string to a float."""
        assert map is True  # noqa: S101
        return (fast_float(y, nan=nan, key=on_fail) for y in x)


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
