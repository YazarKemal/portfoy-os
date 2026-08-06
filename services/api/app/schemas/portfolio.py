from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.enums import DataLatency


class HoldingResponse(BaseModel):
    account_id: uuid.UUID
    account_name: str
    asset_id: uuid.UUID
    asset_code: str
    asset_name: str
    quantity: Decimal
    average_cost: Decimal
    cost_basis: Decimal
    realized_pnl: Decimal
    latest_price: Decimal | None
    price_provider: str | None
    price_market_time: datetime | None
    price_observed_at: datetime | None
    price_latency: DataLatency | None
    market_value: Decimal | None
    unrealized_pnl: Decimal | None
    valuation_status: str  # VALUED | PRICE_MISSING


class HoldingsResponse(BaseModel):
    holdings: list[HoldingResponse]
    count: int


class PortfolioSummaryResponse(BaseModel):
    currency: str
    cash_balance: Decimal
    net_external_contributions: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal | None
    total_market_value: Decimal | None
    total_portfolio_value: Decimal | None
    total_return: Decimal | None
    open_position_count: int
    missing_price_count: int
    account_count: int
    calculated_at: datetime
