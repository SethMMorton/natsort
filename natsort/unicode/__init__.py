"""Pre-determine the collection of unicode decimals, digits, and numerals."""

from __future__ import annotations

import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any, Callable


class UnicodeNumbers:
    """Pre-determine the collection of unicode decimals, digits, and numerals."""

    _numeric_chars: list[str] | None = None
    _digit_chars: list[str] | None = None
    _decimal_chars: list[str] | None = None
    _decimal: str | None = None
    _digits: str | None = None
    _numeric: str | None = None
    _digits_no_decimals: str | None = None
    _numeric_no_decimals: str | None = None

    @classmethod
    def numeric_chars(cls) -> list[str]:
        """Return the list of strings of unicode numerals."""
        if cls._numeric_chars is not None:
            return cls._numeric_chars

        from .numeric_hex import hex_values  # noqa: PLC0415

        cls._numeric_chars = []
        cls._read_chars(cls._numeric_chars, hex_values, unicodedata.numeric)
        return cls._numeric_chars

    @classmethod
    def digit_chars(cls) -> list[str]:
        """Return the list of strings of unicode digits."""
        if cls._digit_chars is not None:
            return cls._digit_chars

        from .digit_hex import hex_values  # noqa: PLC0415

        cls._digit_chars = []
        cls._read_chars(cls._digit_chars, hex_values, unicodedata.digit)
        return cls._digit_chars

    @classmethod
    def decimal_chars(cls) -> list[str]:
        """Return the list of strings of unicode decimals."""
        if cls._decimal_chars is not None:
            return cls._decimal_chars

        from .decimal_hex import hex_values  # noqa: PLC0415

        cls._decimal_chars = []
        cls._read_chars(cls._decimal_chars, hex_values, unicodedata.decimal)
        return cls._decimal_chars

    @classmethod
    def decimal(cls) -> str:
        """Return the string of unicode decimals."""
        if cls._decimal is None:
            cls._decimal = "".join(cls.decimal_chars())
        return cls._decimal

    @classmethod
    def digits(cls) -> str:
        """Return the string of unicode digits."""
        if cls._digits is None:
            cls._digits = "".join(cls.digit_chars())
        return cls._digits

    @classmethod
    def numeric(cls) -> str:
        """Return the string of unicode numerals."""
        if cls._numeric is None:
            cls._numeric = "".join(cls.numeric_chars())
        return cls._numeric

    @classmethod
    def digits_no_decimals(cls) -> str:
        """Return the string of unicode digits that are not decimals."""
        if cls._digits_no_decimals is None:
            cls._digits_no_decimals = "".join(
                [x for x in cls.digits() if x not in cls.decimal()]
            )
        return cls._digits_no_decimals

    @classmethod
    def numeric_no_decimals(cls) -> str:
        """Return the string of unicode numerals that are not decimals."""
        if cls._numeric_no_decimals is None:
            cls._numeric_no_decimals = "".join(
                [x for x in cls.numeric() if x not in cls.decimal()]
            )
        return cls._numeric_no_decimals

    @classmethod
    def _read_chars(
        cls, attr: list[str], values: Iterable[int], func: Callable[[str, Any], Any]
    ) -> None:
        """Read the unicode characters from the hex values."""
        # Convert each hex into the literal Unicode character.
        # Stop if a ValueError is raised in case of a narrow Unicode build.
        # The extra check with unicodedata is in case this Python version
        # does not support some characters.
        for a in values:
            try:
                character = chr(a)
            except ValueError:  # pragma: no cover
                break
            if func(character, None) is None:
                continue  # pragma: no cover
            attr.append(character)
