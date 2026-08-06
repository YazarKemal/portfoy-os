from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_default_user
from app.models import User
from app.schemas.accounts import (
    AccountCreate,
    AccountListResponse,
    AccountResponse,
)
from app.services import accounts as account_service

router = APIRouter(prefix="/api/v1/accounts", tags=["accounts"])


@router.post("", response_model=AccountResponse, status_code=201)
async def create_account(
    body: AccountCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> AccountResponse:
    account = await account_service.create_account(
        db,
        user=user,
        name=body.name,
        currency=body.normalized_currency(),
        institution=body.institution,
        allow_negative_balance=body.allow_negative_balance,
    )
    return AccountResponse.model_validate(account)


@router.get("", response_model=AccountListResponse)
async def list_accounts(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> AccountListResponse:
    accounts = await account_service.list_accounts(db, user=user)
    return AccountListResponse(
        accounts=[AccountResponse.model_validate(a) for a in accounts],
        count=len(accounts),
    )


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> AccountResponse:
    account = await account_service.get_account(db, account_id, user=user)
    return AccountResponse.model_validate(account)
