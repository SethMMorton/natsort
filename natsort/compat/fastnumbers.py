# -*- coding: utf-8 -*-
"""
Interface for natsort to access fastnumbers functions without
having to worry if it is actually installed.
"""
from __future__ import print_function, division, unicode_literals, absolute_import

from distutils.version import StrictVersion

# If the user has fastnumbers installed, they will get great speed
# benefits. If not, we use the simulated functions that come with natsort.
try:
    # noinspection PyPackageRequirements
    from fastnumbers import fast_float, fast_int, __version__ as fn_ver

    # Require >= version 0.7.1.
    if StrictVersion(fn_ver) < StrictVersion("0.7.1"):
        raise ImportError  # pragma: no cover
except ImportError:
    from natsort.compat.fake_fastnumbers import fast_float, fast_int
