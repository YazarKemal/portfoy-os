from __future__ import annotations

from decimal import Decimal

import pytest

from app.domain.money import (
    is_zero,
    quantize_money,
    quantize_price,
    quantize_quantity,
    require_non_negative,
    require_positive,
    safe_decimal,
)


class TestQuantizeMoney:
    def test_rounds_to_4_places(self) -> None:
        assert quantize_money(Decimal("100.12345")) == Decimal("100.1234")
        assert quantize_money(Decimal("100.12344")) == Decimal("100.1234")

    def test_round_half_even(self) -> None:
        # 4th decimal place is 3 (odd), rounds 5 up to 4 → 100.1234
        assert quantize_money(Decimal("100.12335")) == Decimal("100.1234")
        # 4th decimal place is 5 (odd), rounds 6 up to 6 → 100.1236
        assert quantize_money(Decimal("100.12356")) == Decimal("100.1236")

    def test_rejects_nan(self) -> None:
        with pytest.raises(ValueError, match="finite"):
            quantize_money(Decimal("NaN"))

    def test_rejects_infinity(self) -> None:
        with pytest.raises(ValueError, match="finite"):
            quantize_money(Decimal("Infinity"))


class TestQuantizePrice:
    def test_rounds_to_8_places(self) -> None:
        assert quantize_price(Decimal("100.123456789")) == Decimal("100.12345679")
        assert quantize_price(Decimal("100.123456784")) == Decimal("100.12345678")

    def test_rejects_infinity(self) -> None:
        with pytest.raises(ValueError):
            quantize_price(Decimal("-Infinity"))


class TestQuantizeQuantity:
    def test_rounds_to_10_places(self) -> None:
        assert quantize_quantity(Decimal("100.12345678901")) == Decimal("100.1234567890")

    def test_rejects_nan(self) -> None:
        with pytest.raises(ValueError):
            quantize_quantity(Decimal("NaN"))


class TestRequirePositive:
    def test_positive_passes(self) -> None:
        assert require_positive(Decimal("0.0001"), "test") == Decimal("0.0001")

    def test_zero_fails(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            require_positive(Decimal("0"), "test")

    def test_negative_fails(self) -> None:
        with pytest.raises(ValueError, match="positive"):
            require_positive(Decimal("-1"), "test")

    def test_nan_fails(self) -> None:
        with pytest.raises(ValueError):
            require_positive(Decimal("NaN"), "test")


class TestRequireNonNegative:
    def test_zero_passes(self) -> None:
        assert require_non_negative(Decimal("0"), "test") == Decimal("0")

    def test_negative_fails(self) -> None:
        with pytest.raises(ValueError, match="negative"):
            require_non_negative(Decimal("-0.01"), "test")


class TestSafeDecimal:
    def test_from_string(self) -> None:
        assert safe_decimal("100.50") == Decimal("100.50")

    def test_from_decimal(self) -> None:
        assert safe_decimal(Decimal("100.50")) == Decimal("100.50")

    def test_none_fails(self) -> None:
        with pytest.raises(ValueError, match="None"):
            safe_decimal(None)

    def test_invalid_string_fails(self) -> None:
        with pytest.raises(ValueError, match="valid decimal"):
            safe_decimal("not-a-number")

    def test_nan_fails(self) -> None:
        with pytest.raises(ValueError, match="finite"):
            safe_decimal("NaN")


class TestIsZero:
    def test_zero(self) -> None:
        assert is_zero(Decimal("0")) is True
        assert is_zero(Decimal("0.0000")) is True

    def test_non_zero(self) -> None:
        assert is_zero(Decimal("0.0001")) is False
