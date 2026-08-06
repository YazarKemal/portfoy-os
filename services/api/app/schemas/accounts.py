from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    model_config = {"extra": "forbid"}

    name: str = Field(min_length=1, max_length=255)
    institution: str | None = Field(default=None, max_length=255)
    currency: str = Field(default="TRY", min_length=3, max_length=3)
    allow_negative_balance: bool = False

    def normalized_currency(self) -> str:
        return self.currency.upper()


class AccountResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    institution: str | None
    currency: str
    is_active: bool
    allow_negative_balance: bool
    created_at: datetime
    updated_at: datetime


class AccountListResponse(BaseModel):
    accounts: list[AccountResponse]
    count: int
