# -*- coding: utf-8 -*-

from natsort.natsort import (
    as_ascii,
    as_utf8,
    decoder,
    humansorted,
    index_humansorted,
    index_natsorted,
    index_realsorted,
    natsort_key,
    natsort_keygen,
    natsorted,
    ns,
    numeric_regex_chooser,
    order_by_index,
    os_sort_key,
    os_sort_keygen,
    os_sorted,
    realsorted,
)
from natsort.utils import chain_functions

__version__ = "7.1.1"

__all__ = [
    "natsort_key",
    "natsort_keygen",
    "natsorted",
    "humansorted",
    "realsorted",
    "index_natsorted",
    "index_humansorted",
    "index_realsorted",
    "order_by_index",
    "decoder",
    "as_ascii",
    "as_utf8",
    "ns",
    "chain_functions",
    "numeric_regex_chooser",
    "os_sort_key",
    "os_sort_keygen",
    "os_sorted",
]

# Add the ns keys to this namespace for convenience.
globals().update(ns._asdict())
