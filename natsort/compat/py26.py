import mock
import sys

major_minor = sys.version_info[:2]

if major_minor != (2, 6):
    use_hypothesis = True
    from hypothesis import assume, given, example
    from hypothesis.specifiers import (
        integers_in_range,
        integers_from,
        sampled_from,
    )
else:
    example = integers_in_range = integers_from = \
        sampled_from = assume = given = mock.MagicMock()
    use_hypothesis = False
