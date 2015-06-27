# -*- coding: utf-8 -*-
from __future__ import (
    print_function,
    division,
    unicode_literals,
    absolute_import
)

# If the user has fastnumbers installed, they will get great speed
# benefits. If not, we use the simulated functions that come with natsort.
try:
    from fastnumbers import (
        fast_float,
        fast_int,
        isint,
        isfloat,
    )
    import fastnumbers
    v = list(map(int, fastnumbers.__version__.split('.')))
    if not (v[0] >= 0 and v[1] >= 5):  # Require >= version 0.5.0.
        raise ImportError  # pragma: no cover
except ImportError:
    from natsort.compat.fake_fastnumbers import (
        fast_float,
        fast_int,
        isint,
        isfloat,
    )
