from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from app.domain.ledger import (
    AccountState,
    LedgerEvent,
    Position,
    project_state,
    run_ledger,
)
from app.enums import TransactionType


def _make_event(
    transaction_type: TransactionType,
    *,
    account_id: uuid.UUID | None = None,
    asset_id: uuid.UUID | None = None,
    quantity: Decimal | None = None,
    unit_price: Decimal | None = None,
    gross_amount: Decimal | None = None,
    fee_amount: Decimal = Decimal("0"),
    tax_amount: Decimal = Decimal("0"),
    net_cash_effect: Decimal | None = None,
    ts: datetime | None = None,
) -> LedgerEvent:
    aid = account_id or uuid.uuid4()
    ast_id = asset_id or uuid.uuid4()
    qty = quantity or Decimal("0")
    up = unit_price or Decimal("0")

    if gross_amount is None and transaction_type in (
        TransactionType.BUY,
        TransactionType.SELL,
    ):
        ga = qty * up
    else:
        ga = gross_amount or Decimal("0")

    if net_cash_effect is None:
        from app.domain.ledger import _derive_cash_effect

        temp = LedgerEvent(
            id=uuid.uuid4(),
            account_id=aid,
            asset_id=ast_id,
            transaction_type=transaction_type,
            quantity=qty,
            unit_price=up,
            gross_amount=ga,
            fee_amount=fee_amount,
            tax_amount=tax_amount,
            net_cash_effect=Decimal("0"),
            transaction_date=ts or datetime.now(UTC),
            created_at=datetime.now(UTC),
        )
        net_cash_effect = _derive_cash_effect(temp)

    return LedgerEvent(
        id=uuid.uuid4(),
        account_id=aid,
        asset_id=ast_id,
        transaction_type=transaction_type,
        quantity=qty,
        unit_price=up,
        gross_amount=ga,
        fee_amount=fee_amount,
        tax_amount=tax_amount,
        net_cash_effect=net_cash_effect,
        transaction_date=ts or datetime.now(UTC),
        created_at=datetime.now(UTC),
    )


class TestPosition:
    def test_new_position_is_zero(self) -> None:
        pos = Position()
        assert pos.quantity == Decimal("0")
        assert pos.cost_basis == Decimal("0")
        assert pos.average_cost == Decimal("0")
        assert not pos.is_open

    def test_average_cost(self) -> None:
        pos = Position(quantity=Decimal("10"), cost_basis=Decimal("1000.0000"))
        assert pos.average_cost == Decimal("100.0000")

    def test_open_when_positive_quantity(self) -> None:
        pos = Position(quantity=Decimal("1"), cost_basis=Decimal("10"))
        assert pos.is_open


class TestBuy:
    def test_single_buy(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        pos = state.positions[asset_id]
        assert pos.quantity == Decimal("10")
        assert pos.cost_basis == Decimal("1000.0000")
        assert pos.average_cost == Decimal("100.0000")
        assert state.cash_balance == Decimal("-1000.0000")

    def test_buy_with_fee_and_tax(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
            fee_amount=Decimal("5.0000"),
            tax_amount=Decimal("2.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        pos = state.positions[asset_id]
        assert pos.quantity == Decimal("10")
        assert pos.cost_basis == Decimal("1007.0000")
        assert pos.average_cost == Decimal("100.7000")
        assert state.cash_balance == Decimal("-1007.0000")

    def test_two_buys_weighted_average(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()
        t1 = datetime(2026, 1, 1, tzinfo=UTC)
        t2 = datetime(2026, 1, 2, tzinfo=UTC)

        e1 = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
            ts=t1,
        )
        e2 = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("200.00000000"),
            ts=t2,
        )
        states = run_ledger([e1, e2])
        state = states[account_id]
        pos = state.positions[asset_id]
        assert pos.quantity == Decimal("20")
        assert pos.cost_basis == Decimal("3000.0000")
        assert pos.average_cost == Decimal("150.0000")


class TestSell:
    def test_partial_sell(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()
        t1 = datetime(2026, 1, 1, tzinfo=UTC)
        t2 = datetime(2026, 1, 2, tzinfo=UTC)

        buy = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
            ts=t1,
        )
        sell = _make_event(
            TransactionType.SELL,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("5"),
            unit_price=Decimal("150.00000000"),
            ts=t2,
        )
        states = run_ledger([buy, sell])
        state = states[account_id]
        pos = state.positions[asset_id]
        assert pos.quantity == Decimal("5")
        assert pos.cost_basis == Decimal("500.0000")
        assert pos.average_cost == Decimal("100.0000")
        # Cash: -1000 (buy) + 750 (sell) = -250
        assert state.cash_balance == Decimal("-250.0000")
        # Realized P/L: 750 - 500 = 250
        assert state.realized_result == Decimal("250.0000")

    def test_full_sell_zero_position(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()

        buy = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
        )
        sell = _make_event(
            TransactionType.SELL,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("110.00000000"),
        )
        states = run_ledger([buy, sell])
        state = states[account_id]
        assert asset_id not in state.positions or state.positions[asset_id].quantity == Decimal("0")
        assert state.cash_balance == Decimal("100.0000")
        assert state.realized_result == Decimal("100.0000")

    def test_oversell_rejected(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()

        buy = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("5"),
            unit_price=Decimal("100.00000000"),
        )
        sell = _make_event(
            TransactionType.SELL,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
        )
        with pytest.raises(ValueError, match="Insufficient quantity"):
            run_ledger([buy, sell])


class TestDepositWithdrawal:
    def test_deposit_increases_cash_and_contributions(self) -> None:
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.DEPOSIT,
            account_id=account_id,
            gross_amount=Decimal("1000.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("1000.0000")
        assert state.net_external_contributions == Decimal("1000.0000")
        assert state.realized_result == Decimal("0")

    def test_withdrawal_decreases_contributions(self) -> None:
        account_id = uuid.uuid4()
        d = _make_event(
            TransactionType.DEPOSIT,
            account_id=account_id,
            gross_amount=Decimal("1000.0000"),
        )
        w = _make_event(
            TransactionType.WITHDRAWAL,
            account_id=account_id,
            gross_amount=Decimal("300.0000"),
        )
        states = run_ledger([d, w])
        state = states[account_id]
        assert state.cash_balance == Decimal("700.0000")
        assert state.net_external_contributions == Decimal("700.0000")
        assert state.realized_result == Decimal("0")

    def test_deposit_then_buy_cash(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()

        deposit = _make_event(
            TransactionType.DEPOSIT,
            account_id=account_id,
            gross_amount=Decimal("2000.0000"),
        )
        buy = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
        )
        states = run_ledger([deposit, buy])
        state = states[account_id]
        assert state.cash_balance == Decimal("1000.0000")
        assert state.net_external_contributions == Decimal("2000.0000")


class TestIncomeAndCosts:
    def test_dividend_realized(self) -> None:
        account_id = uuid.uuid4()
        asset_id = uuid.uuid4()
        event = _make_event(
            TransactionType.DIVIDEND,
            account_id=account_id,
            asset_id=asset_id,
            gross_amount=Decimal("50.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("50.0000")
        assert state.realized_result == Decimal("50.0000")

    def test_interest_realized(self) -> None:
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.INTEREST,
            account_id=account_id,
            gross_amount=Decimal("30.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("30.0000")
        assert state.realized_result == Decimal("30.0000")

    def test_fee_reduces_cash_and_result(self) -> None:
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.FEE,
            account_id=account_id,
            gross_amount=Decimal("10.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("-10.0000")
        assert state.realized_result == Decimal("-10.0000")

    def test_tax_reduces_cash_and_result(self) -> None:
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.TAX,
            account_id=account_id,
            gross_amount=Decimal("15.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("-15.0000")
        assert state.realized_result == Decimal("-15.0000")


class TestTransfers:
    def test_transfer_in_affects_cash_only(self) -> None:
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.TRANSFER_IN,
            account_id=account_id,
            gross_amount=Decimal("500.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("500.0000")
        assert state.net_external_contributions == Decimal("0")
        assert state.realized_result == Decimal("0")

    def test_transfer_out_affects_cash_only(self) -> None:
        account_id = uuid.uuid4()
        event = _make_event(
            TransactionType.TRANSFER_OUT,
            account_id=account_id,
            gross_amount=Decimal("200.0000"),
        )
        states = run_ledger([event])
        state = states[account_id]
        assert state.cash_balance == Decimal("-200.0000")


class TestEventOrdering:
    def test_ordering_is_deterministic(self) -> None:
        asset_id = uuid.uuid4()
        account_id = uuid.uuid4()
        ts = datetime(2026, 1, 1, tzinfo=UTC)

        e1 = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
            ts=ts,
        )
        e2 = _make_event(
            TransactionType.BUY,
            account_id=account_id,
            asset_id=asset_id,
            quantity=Decimal("10"),
            unit_price=Decimal("200.00000000"),
            ts=ts,
        )
        states1 = run_ledger([e1, e2])
        states2 = run_ledger([e2, e1])
        assert states1[account_id].cash_balance == states2[account_id].cash_balance


class TestCashEffectMismatch:
    def test_mismatch_rejected(self) -> None:
        account_id = uuid.uuid4()
        event = LedgerEvent(
            id=uuid.uuid4(),
            account_id=account_id,
            asset_id=None,
            transaction_type=TransactionType.DEPOSIT,
            quantity=Decimal("0"),
            unit_price=Decimal("0"),
            gross_amount=Decimal("100.0000"),
            fee_amount=Decimal("0"),
            tax_amount=Decimal("0"),
            net_cash_effect=Decimal("999.0000"),  # wrong: should be 100
            transaction_date=datetime.now(UTC),
            created_at=datetime.now(UTC),
        )
        with pytest.raises(ValueError, match="Cash effect mismatch"):
            run_ledger([event])


class TestProjectState:
    def test_buy_projection(self) -> None:
        current = AccountState(cash_balance=Decimal("1000.0000"))
        asset_id = uuid.uuid4()
        projected = project_state(
            current,
            TransactionType.BUY,
            asset_id,
            Decimal("5"),
            Decimal("500.0000"),
            Decimal("0"),
            Decimal("0"),
            Decimal("-500.0000"),
        )
        assert projected.cash_balance == Decimal("500.0000")
        pos = projected.positions[asset_id]
        assert pos.quantity == Decimal("5")
        assert pos.cost_basis == Decimal("500.0000")

    def test_sell_projection(self) -> None:
        asset_id = uuid.uuid4()
        current = AccountState(
            cash_balance=Decimal("0"),
            positions={
                asset_id: Position(quantity=Decimal("10"), cost_basis=Decimal("1000.0000"))
            },
        )
        projected = project_state(
            current,
            TransactionType.SELL,
            asset_id,
            Decimal("5"),
            Decimal("750.0000"),
            Decimal("0"),
            Decimal("0"),
            Decimal("750.0000"),
        )
        assert projected.cash_balance == Decimal("750.0000")
        pos = projected.positions[asset_id]
        assert pos.quantity == Decimal("5")
        assert pos.cost_basis == Decimal("500.0000")
