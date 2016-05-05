# -*- coding: utf-8 -*-
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)
import compat.mock
from natsort.compat.py23 import PY_VERSION

# Use hypothesis if not on python 2.6.
if PY_VERSION > 2.6:
    use_hypothesis = True
    from hypothesis import assume, given, example
    from hypothesis.strategies import (
        sampled_from,
        integers,
        floats,
        tuples,
        lists,
        text,
        binary,
    )
# Otherwise mock these imports, because hypothesis
# is incompatible with python 2.6.
else:
    example = sampled_from = assume = given = floats = integers = \
        tuples = lists = text = binary = compat.mock.MagicMock()
    use_hypothesis = False
