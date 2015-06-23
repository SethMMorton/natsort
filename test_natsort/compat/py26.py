import sys
try:
    import unittest.mock as mock
except ImportError:
    import mock

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
# Otherwise mock these imports.
else:
    example = integers_in_range = integers_from = \
        sampled_from = assume = given = mock.MagicMock()
    use_hypothesis = False
