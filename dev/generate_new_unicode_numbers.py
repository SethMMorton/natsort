#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate the numeric hex list of unicode numerals
"""
import os
import os.path
import sys
import unicodedata

# This is intended to be called from project root. Enforce this.
this_file = os.path.abspath(__file__)
this_base = os.path.basename(this_file)
cwd = os.path.abspath(os.getcwd())
desired_this_file = os.path.join(cwd, "dev", this_base)
if this_file != desired_this_file:
    sys.exit(this_base + " must be called from project root")

# We will write the new numeric hex collection to a natsort package file.
target = os.path.join(cwd, "natsort", "unicode_numeric_hex.py")
with open(target, "w") as fl:
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
            print("    0x{:X},".format(i), file=fl)

    print(")", file=fl)
