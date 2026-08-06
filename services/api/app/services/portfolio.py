from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ledger import run_ledger
from app.enums import TransactionStatus
from app.models import Account, Asset, Transaction, User
from app.services.assets import get_latest_price
from app.services.transactions import _to_ledger_event


async def get_holdings(
    db: AsyncSession, user: User
) -> list[dict[str, Any]]:
    accounts_result = await db.execute(
        select(Account).where(Account.user_id == user.id)
    )
    accounts = list(accounts_result.scalars().all())

    if not accounts:
        return []

    account_ids = [a.id for a in accounts]
    account_map: dict[uuid.UUID, Account] = {a.id: a for a in accounts}

    posted_result = await db.execute(
        select(Transaction)
        .where(
            Transaction.account_id.in_(account_ids),
            Transaction.status == TransactionStatus.POSTED,
        )
        .order_by(
            Transaction.transaction_date,
            Transaction.created_at,
            Transaction.id,
        )
    )
    posted = list(posted_result.scalars().all())

    events = [_to_ledger_event(t) for t in posted]
    states = run_ledger(events)

    holdings: list[dict[str, Any]] = []

    all_asset_ids: set[uuid.UUID] = set()
    for state in states.values():
        all_asset_ids.update(state.positions.keys())

    asset_map: dict[uuid.UUID, Asset] = {}
    if all_asset_ids:
        assets_result = await db.execute(
            select(Asset).where(Asset.id.in_(list(all_asset_ids)))
        )
        for asset in assets_result.scalars().all():
            asset_map[asset.id] = asset

    for account_id, state in states.items():
        account = account_map.get(account_id)
        account_name = account.name if account else "?"

        for asset_id, pos in state.positions.items():
            if not pos.is_open:
                continue

            holding_asset = asset_map.get(asset_id)
            if holding_asset is None:
                continue

            latest_price = await get_latest_price(db, asset_id)

            holding: dict[str, Any] = {
                "account_id": account_id,
                "account_name": account_name,
                "asset_id": asset_id,
                "asset_code": holding_asset.code,
                "asset_name": holding_asset.name,
                "quantity": pos.quantity,
                "average_cost": pos.average_cost,
                "cost_basis": pos.cost_basis,
                "realized_pnl": state.realized_result,
                "latest_price": None,
                "price_provider": None,
                "price_market_time": None,
                "price_observed_at": None,
                "price_latency": None,
                "market_value": None,
                "unrealized_pnl": None,
                "valuation_status": "PRICE_MISSING",
            }

            if latest_price is not None:
                market_value = pos.quantity * latest_price.price
                unrealized_pnl = market_value - pos.cost_basis
                holding.update({
                    "latest_price": latest_price.price,
                    "price_provider": latest_price.provider,
                    "price_market_time": latest_price.market_time,
                    "price_observed_at": latest_price.observed_at,
                    "price_latency": latest_price.data_latency,
                    "market_value": market_value,
                    "unrealized_pnl": unrealized_pnl,
                    "valuation_status": "VALUED",
                })

            holdings.append(holding)

    return holdings


async def get_summary(
    db: AsyncSession, user: User
) -> dict[str, Any]:
    accounts_result = await db.execute(
        select(Account).where(Account.user_id == user.id)
    )
    accounts = list(accounts_result.scalars().all())

    if not accounts:
        return _empty_summary()

    account_ids = [a.id for a in accounts]

    posted_result = await db.execute(
        select(Transaction)
        .where(
            Transaction.account_id.in_(account_ids),
            Transaction.status == TransactionStatus.POSTED,
        )
        .order_by(
            Transaction.transaction_date,
            Transaction.created_at,
            Transaction.id,
        )
    )
    posted = list(posted_result.scalars().all())

    events = [_to_ledger_event(t) for t in posted]
    states = run_ledger(events)

    total_cash = sum(
        (s.cash_balance for s in states.values()), Decimal("0")
    )
    total_contributions = sum(
        (s.net_external_contributions for s in states.values()), Decimal("0")
    )
    total_realized = sum(
        (s.realized_result for s in states.values()), Decimal("0")
    )

    # Gather open positions
    all_asset_ids: set[uuid.UUID] = set()
    for state in states.values():
        for aid, pos in state.positions.items():
            if pos.is_open:
                all_asset_ids.add(aid)

    open_position_count = 0
    missing_price_count = 0
    any_price_missing = False
    total_market_value: Decimal | None = None
    total_unrealized: Decimal | None = None

    # Use first account currency for summary
    currency = accounts[0].currency

    if all_asset_ids:
        total_mv = Decimal("0")
        total_up = Decimal("0")

        for asset_id in all_asset_ids:
            # Find quantity across all accounts
            qty = Decimal("0")
            cb = Decimal("0")
            for state in states.values():
                state_pos = state.positions.get(asset_id)
                if state_pos is not None:
                    qty += state_pos.quantity
                    cb += state_pos.cost_basis

            if qty <= 0:
                continue

            open_position_count += 1
            latest_price = await get_latest_price(db, asset_id)

            if latest_price is None:
                missing_price_count += 1
                any_price_missing = True
            else:
                mv = qty * latest_price.price
                total_mv += mv
                total_up += mv - cb

        if not any_price_missing:
            total_market_value = total_mv
            total_unrealized = total_up

    total_portfolio_value: Decimal | None = None
    total_return: Decimal | None = None
    if total_market_value is not None:
        total_portfolio_value = total_cash + total_market_value
        total_return = total_portfolio_value - total_contributions

    return {
        "currency": currency,
        "cash_balance": total_cash,
        "net_external_contributions": total_contributions,
        "realized_pnl": total_realized,
        "unrealized_pnl": total_unrealized,
        "total_market_value": total_market_value,
        "total_portfolio_value": total_portfolio_value,
        "total_return": total_return,
        "open_position_count": open_position_count,
        "missing_price_count": missing_price_count,
        "account_count": len(accounts),
        "calculated_at": datetime.now(UTC),
    }


def _empty_summary() -> dict[str, Any]:
    return {
        "currency": "TRY",
        "cash_balance": Decimal("0"),
        "net_external_contributions": Decimal("0"),
        "realized_pnl": Decimal("0"),
        "unrealized_pnl": None,
        "total_market_value": None,
        "total_portfolio_value": None,
        "total_return": None,
        "open_position_count": 0,
        "missing_price_count": 0,
        "account_count": 0,
        "calculated_at": datetime.now(UTC),
    }
