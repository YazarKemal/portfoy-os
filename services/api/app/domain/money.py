from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation

MONEY_PRECISION = Decimal("0.0001")  # 4 decimal places
PRICE_PRECISION = Decimal("0.00000001")  # 8 decimal places
QUANTITY_PRECISION = Decimal("0.0000000001")  # 10 decimal places


def _validate_finite(value: Decimal, label: str) -> None:
    if value.is_nan() or value.is_infinite():
        raise ValueError(f"{label} must be a finite number")


def quantize_money(value: Decimal) -> Decimal:
    _validate_finite(value, "Money value")
    return value.quantize(MONEY_PRECISION, rounding=ROUND_HALF_EVEN)


def quantize_price(value: Decimal) -> Decimal:
    _validate_finite(value, "Price value")
    return value.quantize(PRICE_PRECISION, rounding=ROUND_HALF_EVEN)


def quantize_quantity(value: Decimal) -> Decimal:
    _validate_finite(value, "Quantity value")
    return value.quantize(QUANTITY_PRECISION, rounding=ROUND_HALF_EVEN)


def require_positive(value: Decimal, label: str) -> Decimal:
    _validate_finite(value, label)
    if value <= 0:
        raise ValueError(f"{label} must be positive")
    return value


def require_non_negative(value: Decimal, label: str) -> Decimal:
    _validate_finite(value, label)
    if value < 0:
        raise ValueError(f"{label} must not be negative")
    return value


def safe_decimal(value: str | float | Decimal | None, label: str = "value") -> Decimal:
    if value is None:
        raise ValueError(f"{label} must not be None")
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} is not a valid decimal") from None
    _validate_finite(d, label)
    return d


def is_zero(value: Decimal) -> bool:
    return value == 0
