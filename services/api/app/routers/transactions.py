from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_default_user
from app.enums import TransactionStatus, TransactionType
from app.models import User
from app.schemas.transactions import (
    TransactionDraftCreate,
    TransactionDraftResponse,
    TransactionListResponse,
    TransactionResponse,
    TransactionVoidRequest,
)
from app.services import transactions as txn_service

router = APIRouter(prefix="/api/v1/transactions", tags=["transactions"])


@router.post("/drafts", response_model=TransactionDraftResponse, status_code=201)
async def create_draft(
    body: TransactionDraftCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> TransactionDraftResponse:
    txn, current, projected, warnings = await txn_service.create_draft(
        db,
        user=user,
        account_id=body.account_id,
        asset_id=body.asset_id,
        transaction_type=body.transaction_type,
        quantity=body.quantity,
        unit_price=body.unit_price,
        gross_amount=body.gross_amount,
        fee_amount=body.fee_amount,
        tax_amount=body.tax_amount,
        currency=body.normalized_currency(),
        transaction_date=body.transaction_date,
        source=body.source,
        idempotency_key=body.idempotency_key,
        notes=body.notes,
    )

    # Build projected quantity for trade types
    projected_qty: Decimal | None = None

    if body.asset_id is not None and body.transaction_type in (
        TransactionType.BUY,
        TransactionType.SELL,
    ):
        from app.domain.ledger import Position

        pos = current.positions.get(body.asset_id, Position())
        if body.transaction_type == TransactionType.BUY:
            projected_qty = pos.quantity + (body.quantity or Decimal("0"))
        elif body.transaction_type == TransactionType.SELL:
            projected_qty = pos.quantity - (body.quantity or Decimal("0"))

    return TransactionDraftResponse(
        id=txn.id,
        account_id=txn.account_id,
        asset_id=txn.asset_id,
        transaction_type=txn.transaction_type,
        status=txn.status,
        source=txn.source,
        quantity=txn.quantity,
        unit_price=txn.unit_price,
        gross_amount=txn.gross_amount,
        fee_amount=txn.fee_amount,
        tax_amount=txn.tax_amount,
        net_cash_effect=txn.net_cash_effect,
        currency=txn.currency,
        transaction_date=txn.transaction_date,
        idempotency_key=txn.idempotency_key,
        notes=txn.notes,
        confirmed_at=txn.confirmed_at,
        voided_at=txn.voided_at,
        void_reason=txn.void_reason,
        created_at=txn.created_at,
        updated_at=txn.updated_at,
        projected_cash_balance=projected.cash_balance,
        projected_quantity=projected_qty,
        warnings=warnings,
    )


@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    account_id: uuid.UUID | None = Query(default=None),
    asset_id: uuid.UUID | None = Query(default=None),
    transaction_type: TransactionType | None = Query(default=None),
    status: TransactionStatus | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> TransactionListResponse:
    transactions, total = await txn_service.list_transactions(
        db,
        user=user,
        account_id=account_id,
        asset_id=asset_id,
        transaction_type=transaction_type,
        status=status,
        limit=limit,
        offset=offset,
    )
    return TransactionListResponse(
        transactions=[TransactionResponse.model_validate(t) for t in transactions],
        count=total,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> TransactionResponse:
    txn = await txn_service.get_transaction(db, transaction_id, user=user)
    return TransactionResponse.model_validate(txn)


@router.post("/{transaction_id}/confirm", response_model=TransactionResponse)
async def confirm_transaction(
    transaction_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> TransactionResponse:
    txn = await txn_service.confirm_transaction(db, transaction_id, user=user)
    return TransactionResponse.model_validate(txn)


@router.post("/{transaction_id}/void", response_model=TransactionResponse)
async def void_transaction(
    transaction_id: uuid.UUID,
    body: TransactionVoidRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_default_user),
) -> TransactionResponse:
    txn = await txn_service.void_transaction(db, transaction_id, body.reason, user=user)
    return TransactionResponse.model_validate(txn)
