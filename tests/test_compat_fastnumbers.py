"""Test the fastnumbers compatibility layer."""

from __future__ import annotations

from decimal import Decimal

from natsort.compat.fastnumbers import try_float


def test_try_float_widens_overflowing_magnitude_to_decimal_example() -> None:
    # "1e400" and "1e500" both overflow float()'s range to inf, so if the
    # backend's raw result were used as-is they would compare equal and
    # lose their real order. This must hold regardless of whether the
    # real fastnumbers package (any supported version) or natsort's own
    # fallback is providing the underlying conversion.
    small, large = try_float(["1e400", "1e500"], map=True)
    assert isinstance(small, Decimal)
    assert isinstance(large, Decimal)
    assert small != large
    assert small < large


def test_try_float_orders_reversed_overflowing_magnitudes_too() -> None:
    # Same as above, but make sure the result doesn't just happen to match
    # because of the order the values were given in.
    large, small = try_float(["1e500", "1e400"], map=True)
    assert isinstance(small, Decimal)
    assert isinstance(large, Decimal)
    assert small < large


def test_try_float_still_returns_a_plain_float_for_literal_infinity() -> None:
    # A string that spells out infinity is not the result of an overflow,
    # so it should still come back as a plain float, same as before.
    pos_inf, neg_inf = try_float(["inf", "-inf"], map=True)
    assert pos_inf == float("inf")
    assert neg_inf == float("-inf")
    assert isinstance(pos_inf, float)
    assert isinstance(neg_inf, float)


def test_try_float_nan_substitution_is_not_treated_as_overflow() -> None:
    # The "nan" substitution value can legitimately be +/-inf (depending on
    # ns.NANLAST), and that is a deliberate substitution, not an overflow,
    # so it must not get widened to Decimal.
    (result,) = try_float(["nan"], map=True, nan=float("-inf"))
    assert result == float("-inf")
    assert isinstance(result, float)
