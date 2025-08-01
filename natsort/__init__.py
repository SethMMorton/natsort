"""Public interface for the natsort package."""

from __future__ import annotations

try:
    # The redundant "as" tells mypy to treat as explict import
    from natsort._version import __version__ as __version__
    from natsort._version import __version_tuple__ as __version_tuple__
except ImportError:
    __version__ = "unknown version"
    __version_tuple__ = (0, 0, "unknown version")
from natsort.natsort import (
    NatsortKeyType,
    OSSortKeyType,
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
    numeric_regex_chooser,
    order_by_index,
    os_sort_key,
    os_sort_keygen,
    os_sorted,
    realsorted,
)
from natsort.ns_enum import NSType, ns
from natsort.utils import KeyType, NatsortInType, NatsortOutType, chain_functions

__all__ = [
    "KeyType",
    "NSType",
    "NatsortInType",
    "NatsortKeyType",
    "NatsortOutType",
    "OSSortKeyType",
    "as_ascii",
    "as_utf8",
    "chain_functions",
    "decoder",
    "humansorted",
    "index_humansorted",
    "index_natsorted",
    "index_realsorted",
    "natsort_key",
    "natsort_keygen",
    "natsorted",
    "ns",
    "numeric_regex_chooser",
    "order_by_index",
    "os_sort_key",
    "os_sort_keygen",
    "os_sorted",
    "realsorted",
]

# Add the ns keys to this namespace for convenience.
globals().update(dict(ns.__members__.items()))
