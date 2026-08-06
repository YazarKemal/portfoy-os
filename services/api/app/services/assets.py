from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums import DataLatency
from app.errors import DomainError
from app.models import Asset, AssetPrice


async def create_asset(
    db: AsyncSession,
    code: str,
    name: str,
    asset_type: str,
    currency: str = "TRY",
) -> Asset:
    if not code.strip() or not name.strip():
        raise DomainError(
            "INVALID_TRANSACTION_SHAPE",
            "Varlık kodu ve adı boş olamaz.",
        )

    asset = Asset(
        code=code.strip().upper(),
        name=name.strip(),
        asset_type=asset_type.strip().lower(),
        currency=currency.upper(),
    )
    db.add(asset)
    await db.flush()
    await db.refresh(asset)
    return asset


async def list_assets(db: AsyncSession) -> list[Asset]:
    result = await db.execute(
        select(Asset).order_by(Asset.created_at.desc())
    )
    return list(result.scalars().all())


async def get_asset(db: AsyncSession, asset_id: uuid.UUID) -> Asset:
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if asset is None:
        raise DomainError("ASSET_NOT_FOUND", f"Varlık bulunamadı: {asset_id}")
    return asset


async def add_manual_price(
    db: AsyncSession,
    asset_id: uuid.UUID,
    price: str,
    currency: str,
    market_time: datetime,
) -> AssetPrice:
    # Verify asset exists
    await get_asset(db, asset_id)

    if market_time.tzinfo is None:
        market_time = market_time.replace(tzinfo=UTC)

    asset_price = AssetPrice(
        asset_id=asset_id,
        price=price,
        currency=currency.upper(),
        provider="manual",
        market_time=market_time,
        data_latency=DataLatency.MANUAL,
        observed_at=datetime.now(UTC),
    )
    db.add(asset_price)
    await db.flush()
    await db.refresh(asset_price)
    return asset_price


async def get_latest_price(
    db: AsyncSession, asset_id: uuid.UUID
) -> AssetPrice | None:
    result = await db.execute(
        select(AssetPrice)
        .where(AssetPrice.asset_id == asset_id)
        .order_by(
            AssetPrice.market_time.desc(),
            AssetPrice.observed_at.desc(),
            AssetPrice.id.desc(),
        )
        .limit(1)
    )
    return result.scalar_one_or_none()
