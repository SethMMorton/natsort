# -*- coding: utf-8 -*-
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)
import sys
import compat.mock

major_minor = sys.version_info[:2]

# Use hypothesis if not on python 2.6.
if major_minor != (2, 6):
    use_hypothesis = True
    from hypothesis import assume, given, example
    from hypothesis.specifiers import (
        integers_in_range,
        integers_from,
        sampled_from,
    )
# Otherwise mock these imports, because hypothesis
# is incompatible with python 2.6.
else:
    example = integers_in_range = integers_from = \
        sampled_from = assume = given = compat.mock.MagicMock()
    use_hypothesis = False
