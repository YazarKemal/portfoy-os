from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_default_user
from app.models import User
from app.schemas.portfolio import (
    HoldingResponse,
    HoldingsResponse,
    PortfolioSummaryResponse,
)
from app.services import portfolio as portfolio_service

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])


@router.get("/summary", response_model=PortfolioSummaryResponse)
async def get_summary(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> PortfolioSummaryResponse:
    summary = await portfolio_service.get_summary(db, user=user)
    return PortfolioSummaryResponse(**summary)


@router.get("/holdings", response_model=HoldingsResponse)
async def get_holdings(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> HoldingsResponse:
    raw_holdings = await portfolio_service.get_holdings(db, user=user)
    holdings = [HoldingResponse(**h) for h in raw_holdings]
    return HoldingsResponse(
        holdings=holdings,
        count=len(holdings),
    )
