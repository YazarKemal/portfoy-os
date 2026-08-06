from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.domain.money import quantize_money
from app.enums import TransactionType


@dataclass
class Position:
    quantity: Decimal = Decimal("0")
    cost_basis: Decimal = Decimal("0")

    @property
    def average_cost(self) -> Decimal:
        if self.quantity == 0:
            return Decimal("0")
        return quantize_money(self.cost_basis / self.quantity)

    @property
    def is_open(self) -> bool:
        return self.quantity > 0


@dataclass
class AccountState:
    cash_balance: Decimal = Decimal("0")
    net_external_contributions: Decimal = Decimal("0")
    realized_result: Decimal = Decimal("0")
    positions: dict[uuid.UUID, Position] = field(default_factory=dict)

    def get_position(self, asset_id: uuid.UUID) -> Position:
        if asset_id not in self.positions:
            self.positions[asset_id] = Position()
        return self.positions[asset_id]

    def apply_event(self, event: LedgerEvent) -> None:
        expected_cash = _derive_cash_effect(event)
        if event.net_cash_effect != expected_cash:
            raise ValueError(
                f"Cash effect mismatch for event {event.id}: "
                f"stored={event.net_cash_effect}, derived={expected_cash}"
            )

        t = event.transaction_type

        if t == TransactionType.BUY:
            if event.asset_id is None:
                raise ValueError(f"BUY event {event.id} missing asset_id")
            pos = self.get_position(event.asset_id)
            pos.quantity += event.quantity
            pos.cost_basis += event.gross_amount + event.fee_amount + event.tax_amount
            self.cash_balance += event.net_cash_effect

        elif t == TransactionType.SELL:
            if event.asset_id is None:
                raise ValueError(f"SELL event {event.id} missing asset_id")
            pos = self.get_position(event.asset_id)
            if event.quantity > pos.quantity:
                raise ValueError(
                    f"Insufficient quantity for {event.id}: "
                    f"have {pos.quantity}, selling {event.quantity}"
                )
            allocated_cost = quantize_money(pos.average_cost * event.quantity)
            realized = event.net_cash_effect - allocated_cost
            pos.quantity -= event.quantity
            pos.cost_basis -= allocated_cost
            self.cash_balance += event.net_cash_effect
            self.realized_result += realized

        elif t in (TransactionType.DIVIDEND, TransactionType.INTEREST):
            self.cash_balance += event.net_cash_effect
            self.realized_result += event.net_cash_effect

        elif t == TransactionType.DEPOSIT:
            self.cash_balance += event.net_cash_effect
            self.net_external_contributions += event.gross_amount

        elif t == TransactionType.WITHDRAWAL:
            self.cash_balance += event.net_cash_effect
            self.net_external_contributions -= event.gross_amount

        elif t in (TransactionType.FEE, TransactionType.TAX):
            self.cash_balance += event.net_cash_effect
            self.realized_result += event.net_cash_effect

        elif t in (TransactionType.TRANSFER_IN, TransactionType.TRANSFER_OUT):
            self.cash_balance += event.net_cash_effect


@dataclass
class LedgerEvent:
    id: uuid.UUID
    account_id: uuid.UUID
    asset_id: uuid.UUID | None
    transaction_type: TransactionType
    quantity: Decimal
    unit_price: Decimal
    gross_amount: Decimal
    fee_amount: Decimal
    tax_amount: Decimal
    net_cash_effect: Decimal
    transaction_date: datetime
    created_at: datetime

    def sort_key(self) -> tuple[datetime, datetime, uuid.UUID]:
        return (self.transaction_date, self.created_at, self.id)


def run_ledger(events: list[LedgerEvent]) -> dict[uuid.UUID, AccountState]:
    states: dict[uuid.UUID, AccountState] = {}
    sorted_events = sorted(events, key=lambda e: e.sort_key())

    for event in sorted_events:
        if event.account_id not in states:
            states[event.account_id] = AccountState()
        states[event.account_id].apply_event(event)

    return states


def project_state(
    current: AccountState,
    event_type: TransactionType,
    asset_id: uuid.UUID | None,
    quantity: Decimal | None,
    gross_amount: Decimal,
    fee_amount: Decimal,
    tax_amount: Decimal,
    net_cash_effect: Decimal,
) -> AccountState:
    """Return a projected AccountState without verifying net_cash_effect.

    This is used for previews before a transaction is persisted, so unit_price
    may not be available independently to recompute the cash effect.
    """
    projected = AccountState(
        cash_balance=current.cash_balance,
        net_external_contributions=current.net_external_contributions,
        realized_result=current.realized_result,
        positions={
            aid: Position(quantity=pos.quantity, cost_basis=pos.cost_basis)
            for aid, pos in current.positions.items()
        },
    )

    t = event_type
    qty = quantity or Decimal("0")

    if t == TransactionType.BUY:
        if asset_id is None:
            raise ValueError("BUY projection missing asset_id")
        pos = projected.get_position(asset_id)
        pos.quantity += qty
        pos.cost_basis += gross_amount + fee_amount + tax_amount
        projected.cash_balance += net_cash_effect

    elif t == TransactionType.SELL:
        if asset_id is None:
            raise ValueError("SELL projection missing asset_id")
        pos = projected.get_position(asset_id)
        allocated_cost = quantize_money(pos.average_cost * qty)
        realized = net_cash_effect - allocated_cost
        pos.quantity -= qty
        pos.cost_basis -= allocated_cost
        projected.cash_balance += net_cash_effect
        projected.realized_result += realized

    elif t in (TransactionType.DIVIDEND, TransactionType.INTEREST):
        projected.cash_balance += net_cash_effect
        projected.realized_result += net_cash_effect

    elif t == TransactionType.DEPOSIT:
        projected.cash_balance += net_cash_effect
        projected.net_external_contributions += gross_amount

    elif t == TransactionType.WITHDRAWAL:
        projected.cash_balance += net_cash_effect
        projected.net_external_contributions -= gross_amount

    elif t in (TransactionType.FEE, TransactionType.TAX):
        projected.cash_balance += net_cash_effect
        projected.realized_result += net_cash_effect

    elif t in (TransactionType.TRANSFER_IN, TransactionType.TRANSFER_OUT):
        projected.cash_balance += net_cash_effect

    return projected


def _derive_cash_effect(event: LedgerEvent) -> Decimal:
    t = event.transaction_type

    if t == TransactionType.BUY:
        gross = event.quantity * event.unit_price
        return quantize_money(-(gross + event.fee_amount + event.tax_amount))

    elif t == TransactionType.SELL:
        gross = event.quantity * event.unit_price
        return quantize_money(gross - event.fee_amount - event.tax_amount)

    elif t in (TransactionType.DIVIDEND, TransactionType.INTEREST):
        return quantize_money(event.gross_amount - event.fee_amount - event.tax_amount)

    elif t == TransactionType.DEPOSIT:
        return quantize_money(event.gross_amount)

    elif t == TransactionType.WITHDRAWAL or t in (TransactionType.FEE, TransactionType.TAX):
        return quantize_money(-event.gross_amount)

    elif t == TransactionType.TRANSFER_IN:
        return quantize_money(event.gross_amount)

    elif t == TransactionType.TRANSFER_OUT:
        return quantize_money(-event.gross_amount)

    raise ValueError(f"Unknown transaction type: {t}")
