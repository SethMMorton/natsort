#! /usr/bin/env python3
"""Generate the numeric hex list of unicode numerals."""

from __future__ import annotations

import json
import pathlib
import sys
import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

# This is intended to be called from project root. Enforce this.
this_file = pathlib.Path(__file__).absolute()
this_base = this_file.name
cwd = pathlib.Path.cwd().absolute()
desired_this_file = cwd / "dev" / this_base
if this_file != desired_this_file:
    sys.exit(this_base + " must be called from project root")


def unicode_seive() -> Iterator[int]:
    """Yield all unicode code points that are numerals."""
    for i in range(0x110000):
        try:
            a = chr(i)
        except ValueError:
            return
        if a in "0123456789":
            continue
        if unicodedata.numeric(a, None) is not None:
            yield i


# We will write the new numeric hex collection to a natsort package file.
target_file = cwd / "natsort" / "unicode_numeric_hex.json"
with target_file.open("w") as fl:
    json.dump(list(unicode_seive()), fl, indent=4)
