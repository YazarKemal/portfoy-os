from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.enums import TransactionSource, TransactionStatus, TransactionType


class TransactionDraftCreate(BaseModel):
    model_config = {"extra": "forbid"}

    account_id: uuid.UUID
    asset_id: uuid.UUID | None = None
    transaction_type: TransactionType
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    gross_amount: Decimal | None = None
    fee_amount: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    currency: str = Field(default="TRY", min_length=3, max_length=3)
    transaction_date: datetime
    source: TransactionSource = TransactionSource.MANUAL
    idempotency_key: str | None = Field(default=None, max_length=100)
    notes: str | None = None

    def normalized_currency(self) -> str:
        return self.currency.upper()


class TransactionDraftResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    account_id: uuid.UUID
    asset_id: uuid.UUID | None
    transaction_type: TransactionType
    status: TransactionStatus
    source: TransactionSource
    quantity: Decimal | None
    unit_price: Decimal | None
    gross_amount: Decimal
    fee_amount: Decimal
    tax_amount: Decimal
    net_cash_effect: Decimal
    currency: str
    transaction_date: datetime
    idempotency_key: str | None
    notes: str | None
    confirmed_at: datetime | None
    voided_at: datetime | None
    void_reason: str | None
    created_at: datetime
    updated_at: datetime
    # Review summary
    projected_cash_balance: Decimal | None = None
    projected_quantity: Decimal | None = None
    warnings: list[str] = Field(default_factory=list)


class TransactionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    account_id: uuid.UUID
    asset_id: uuid.UUID | None
    transaction_type: TransactionType
    status: TransactionStatus
    source: TransactionSource
    quantity: Decimal | None
    unit_price: Decimal | None
    gross_amount: Decimal
    fee_amount: Decimal
    tax_amount: Decimal
    net_cash_effect: Decimal
    currency: str
    transaction_date: datetime
    idempotency_key: str | None
    notes: str | None
    confirmed_at: datetime | None
    voided_at: datetime | None
    void_reason: str | None
    created_at: datetime
    updated_at: datetime


class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]
    count: int


class TransactionVoidRequest(BaseModel):
    model_config = {"extra": "forbid"}

    reason: str = Field(min_length=1)
