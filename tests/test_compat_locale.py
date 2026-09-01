"""Test the locale compatibility layer."""

from __future__ import annotations

import importlib.util
import sys
import types
from typing import TYPE_CHECKING

import pytest

import natsort.compat.locale

if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture
def icu_locale_module() -> Iterator[types.ModuleType]:
    """Load natsort/compat/locale.py with a stub "icu" module in place."""
    saved = sys.modules.get("icu")
    sys.modules["icu"] = types.ModuleType("icu")
    spec = importlib.util.spec_from_file_location(
        "_icu_locale", natsort.compat.locale.__file__
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        yield module
    finally:
        if saved is None:
            del sys.modules["icu"]
        else:
            sys.modules["icu"] = saved


def test_icu_null_string_locale_max_sorts_after_any_bytes(
    icu_locale_module: types.ModuleType,
) -> None:
    # Prepended to numbers under ns.NUMAFTER | ns.LOCALE, so it must sort
    # after every sort key PyICU can return.
    assert icu_locale_module.null_string_locale_max > b"\xff" * 49
    assert icu_locale_module.null_string_locale_max > b"\xfe" * 100
