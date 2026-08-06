from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.assets import (
    AssetCreate,
    AssetListResponse,
    AssetPriceCreate,
    AssetPriceResponse,
    AssetResponse,
)
from app.services import assets as asset_service

router = APIRouter(prefix="/api/v1/assets", tags=["assets"])


@router.post("", response_model=AssetResponse, status_code=201)
async def create_asset(
    body: AssetCreate,
    db: AsyncSession = Depends(get_db),
) -> AssetResponse:
    asset = await asset_service.create_asset(
        db,
        code=body.normalized_code(),
        name=body.name,
        asset_type=body.asset_type,
        currency=body.normalized_currency(),
    )
    return AssetResponse.model_validate(asset)


@router.get("", response_model=AssetListResponse)
async def list_assets(
    db: AsyncSession = Depends(get_db),
) -> AssetListResponse:
    assets = await asset_service.list_assets(db)
    return AssetListResponse(
        assets=[AssetResponse.model_validate(a) for a in assets],
        count=len(assets),
    )


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> AssetResponse:
    asset = await asset_service.get_asset(db, asset_id)
    return AssetResponse.model_validate(asset)


@router.post("/{asset_id}/prices", response_model=AssetPriceResponse, status_code=201)
async def add_asset_price(
    asset_id: uuid.UUID,
    body: AssetPriceCreate,
    db: AsyncSession = Depends(get_db),
) -> AssetPriceResponse:
    price = await asset_service.add_manual_price(
        db,
        asset_id=asset_id,
        price=str(body.price),
        currency=body.normalized_currency(),
        market_time=body.market_time,
    )
    return AssetPriceResponse.model_validate(price)


@router.get("/{asset_id}/prices/latest", response_model=AssetPriceResponse | None)
async def get_latest_price(
    asset_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> AssetPriceResponse | None:
    price = await asset_service.get_latest_price(db, asset_id)
    if price is None:
        return None
    return AssetPriceResponse.model_validate(price)
