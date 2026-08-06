from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.enums import DataLatency


class AssetCreate(BaseModel):
    model_config = {"extra": "forbid"}

    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    asset_type: str = Field(min_length=1, max_length=50)
    currency: str = Field(default="TRY", min_length=3, max_length=3)

    def normalized_code(self) -> str:
        return self.code.upper()

    def normalized_currency(self) -> str:
        return self.currency.upper()


class AssetResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    code: str
    name: str
    asset_type: str
    currency: str
    created_at: datetime
    updated_at: datetime


class AssetListResponse(BaseModel):
    assets: list[AssetResponse]
    count: int


class AssetPriceCreate(BaseModel):
    model_config = {"extra": "forbid"}

    price: Decimal
    currency: str = Field(default="TRY", min_length=3, max_length=3)
    market_time: datetime

    def normalized_currency(self) -> str:
        return self.currency.upper()


class AssetPriceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    asset_id: uuid.UUID
    price: Decimal
    currency: str
    provider: str
    market_time: datetime
    observed_at: datetime
    data_latency: DataLatency
    created_at: datetime
