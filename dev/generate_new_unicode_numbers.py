#! /usr/bin/env python
"""Generate the numeric hex list of unicode numerals."""

from __future__ import annotations

import pathlib
import sys
import unicodedata

# This is intended to be called from project root. Enforce this.
this_file = pathlib.Path(__file__).absolute()
this_base = this_file.name
cwd = pathlib.Path.cwd().absolute()
desired_this_file = cwd / "dev" / this_base
if this_file != desired_this_file:
    sys.exit(this_base + " must be called from project root")

# We will write the new numeric hex collection to a natsort package file.
target = cwd / "natsort" / "unicode_numeric_hex.py"
with target.open("w") as fl:
    print(
        '''# -*- coding: utf-8 -*-
"""
Contains all possible non-ASCII unicode numbers.
"""

# Rather than determine what unicode characters are numeric on the fly which
# would incur a startup runtime penalty, the hex values are hard-coded below.
numeric_hex = (''',
        file=fl,
    )

    # Write out each individual hex value.
    for i in range(0x110000):
        try:
            a = chr(i)
        except ValueError:
            break
        if a in "0123456789":
            continue
        if unicodedata.numeric(a, None) is not None:
            print(f"    0x{i:X},", file=fl)

    print(")", file=fl)
