# -*- coding: utf-8 -*-

try:
    from pathlib import PurePath  # PurePath is the base object for Paths.
except ImportError:  # pragma: no cover
    PurePath = object  # To avoid NameErrors.
    has_pathlib = False
else:
    has_pathlib = True
