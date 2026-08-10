#! /usr/bin/env python3
"""Generate the numeric hex list of unicode numerals."""

from __future__ import annotations

import pathlib
import sys
import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from typing import Any

# This is intended to be called from project root. Enforce this.
this_file = pathlib.Path(__file__).absolute()
this_base = this_file.name
cwd = pathlib.Path.cwd().absolute()
desired_this_file = cwd / "dev" / this_base
if this_file != desired_this_file:
    sys.exit(this_base + " must be called from project root")


def unicode_seive(predicate: Callable[[str, Any], Any]) -> Iterator[int]:
    """Yield all unicode code points that are numerals."""
    for i in range(0x110000):
        try:
            a = chr(i)
        except ValueError:
            return
        if a in "0123456789":
            continue
        if predicate(a, None) is not None:
            yield i


# Collect all the hex values for unicode numbers.
combinations = [
    (unicode_seive(unicodedata.decimal), "decimal"),
    (unicode_seive(unicodedata.digit), "digit"),
    (unicode_seive(unicodedata.numeric), "numeric"),
]
for seive, name in combinations:
    target_file = cwd / "natsort" / "unicode" / f"{name}_hex.py"
    with target_file.open("w") as fl:
        print(
            f'''"""Contains all possible non-ASCII unicode {name}s."""

# Rather than determine what unicode characters are {name}s on the fly which
# would incur a startup runtime penalty, the hex values are hard-coded below.
hex_values: tuple[int, ...] = (''',
            file=fl,
        )
        for i in seive:
            print(f"    0x{i:X},", file=fl)
        print(")", file=fl)
