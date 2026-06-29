"""Pre-determine the collection of unicode decimals, digits, and numerals."""

from __future__ import annotations

import importlib.resources
import json
import unicodedata


class UnicodeNumbers:
    """Pre-determine the collection of unicode decimals, digits, and numerals."""

    _numeric_hex: list[int] | None = None
    _numeric_chars: list[str] | None = None
    _digit_chars: list[str] | None = None
    _decimal_chars: list[str] | None = None
    _decimal: str | None = None
    _digits: str | None = None
    _numeric: str | None = None
    _digits_no_decimals: str | None = None
    _numeric_no_decimals: str | None = None

    @classmethod
    def numeric_hex(cls) -> list[int]:
        """Load the numeric hex values from the JSON file."""
        if cls._numeric_hex is None:
            with importlib.resources.open_text(
                "natsort", "unicode_numeric_hex.json"
            ) as fl:
                cls._numeric_hex = json.load(fl)
                assert isinstance(cls._numeric_hex, list)  # noqa: S101
        return cls._numeric_hex

    @classmethod
    def numeric_chars(cls) -> list[str]:
        """Return the list of strings of unicode numerals."""
        if cls._numeric_chars is None:
            cls._populate_unicode_strings()
        assert cls._numeric_chars is not None  # noqa: S101
        return cls._numeric_chars

    @classmethod
    def digit_chars(cls) -> list[str]:
        """Return the list of strings of unicode digits."""
        if cls._digit_chars is None:
            cls._populate_unicode_strings()
        assert cls._digit_chars is not None  # noqa: S101
        return cls._digit_chars

    @classmethod
    def decimal_chars(cls) -> list[str]:
        """Return the list of strings of unicode decimals."""
        if cls._decimal_chars is None:
            cls._populate_unicode_strings()
        assert cls._decimal_chars is not None  # noqa: S101
        return cls._decimal_chars

    @classmethod
    def decimal(cls) -> str:
        """Return the string of unicode decimals."""
        if cls._decimal is None:
            cls._populate_unicode_strings()
        assert cls._decimal is not None  # noqa: S101
        return cls._decimal

    @classmethod
    def digits(cls) -> str:
        """Return the string of unicode digits."""
        if cls._digits is None:
            cls._populate_unicode_strings()
        assert cls._digits is not None  # noqa: S101
        return cls._digits

    @classmethod
    def numeric(cls) -> str:
        """Return the string of unicode numerals."""
        if cls._numeric is None:
            cls._populate_unicode_strings()
        assert cls._numeric is not None  # noqa: S101
        return cls._numeric

    @classmethod
    def digits_no_decimals(cls) -> str:
        """Return the string of unicode digits that are not decimals."""
        if cls._digits_no_decimals is None:
            cls._populate_unicode_strings()
        assert cls._digits_no_decimals is not None  # noqa: S101
        return cls._digits_no_decimals

    @classmethod
    def numeric_no_decimals(cls) -> str:
        """Return the string of unicode numerals that are not decimals."""
        if cls._numeric_no_decimals is None:
            cls._populate_unicode_strings()
        assert cls._numeric_no_decimals is not None  # noqa: S101
        return cls._numeric_no_decimals

    @classmethod
    def _populate_unicode_strings(cls) -> None:
        """Populate digits_no_decimals and numeric_no_decimals."""
        # Convert each hex into the literal Unicode character.
        # Stop if a ValueError is raised in case of a narrow Unicode build.
        # The extra check with unicodedata is in case this Python version
        # does not support some characters.
        cls._numeric_chars = []
        for a in cls.numeric_hex():
            try:
                character = chr(a)
            except ValueError:  # pragma: no cover
                break
            if unicodedata.numeric(character, None) is None:
                continue  # pragma: no cover
            cls._numeric_chars.append(character)

        # The digit characters are a subset of the numerals.
        cls._digit_chars = [
            a for a in cls._numeric_chars if unicodedata.digit(a, None) is not None
        ]

        # The decimal characters are a subset of the numerals
        # (probably of the digits, but let's be safe).
        cls._decimal_chars = [
            a for a in cls._numeric_chars if unicodedata.decimal(a, None) is not None
        ]

        # Create a single string with the above data.
        cls._decimal = "".join(cls._decimal_chars)
        cls._digits = "".join(cls._digit_chars)
        cls._numeric = "".join(cls._numeric_chars)
        cls._digits_no_decimals = "".join(
            [x for x in cls._digits if x not in cls._decimal]
        )
        cls._numeric_no_decimals = "".join(
            [x for x in cls._numeric if x not in cls._decimal]
        )
