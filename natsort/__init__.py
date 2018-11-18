# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import warnings

from natsort.natsort import (
    as_ascii,
    as_utf8,
    decoder,
    humansorted,
    index_humansorted,
    index_natsorted,
    index_realsorted,
    index_versorted,
    natsort_key,
    natsort_keygen,
    natsorted,
    ns,
    order_by_index,
    realsorted,
    versorted,
)
from natsort.utils import chain_functions

if float(sys.version[:3]) < 3:
    from natsort.natsort import natcmp

__version__ = "5.5.0"

__all__ = [
    "natsort_key",
    "natsort_keygen",
    "natsorted",
    "versorted",
    "humansorted",
    "realsorted",
    "index_natsorted",
    "index_versorted",
    "index_humansorted",
    "index_realsorted",
    "order_by_index",
    "decoder",
    "natcmp",
    "as_ascii",
    "as_utf8",
    "ns",
    "chain_functions",
]

# Add the ns keys to this namespace for convenience.
# A dict comprehension is not used for Python 2.6 compatibility.
# We catch warnings from the deprecated ns enum values when adding
# them to natsort's main namespace.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    globals().update(dict((k, getattr(ns, k)) for k in dir(ns) if k.isupper()))
