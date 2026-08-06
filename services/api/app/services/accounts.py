from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import DomainError
from app.models import Account, User


async def create_account(
    db: AsyncSession,
    user: User,
    name: str,
    currency: str,
    institution: str | None = None,
    allow_negative_balance: bool = False,
) -> Account:
    if not name.strip():
        raise DomainError(
            "INVALID_TRANSACTION_SHAPE",
            "Hesap adı boş olamaz.",
        )

    account = Account(
        user_id=user.id,
        name=name.strip(),
        currency=currency.upper(),
        institution=institution.strip() if institution else None,
        allow_negative_balance=allow_negative_balance,
    )
    db.add(account)
    await db.flush()
    await db.refresh(account)
    return account


async def list_accounts(db: AsyncSession, user: User) -> list[Account]:
    result = await db.execute(
        select(Account).where(Account.user_id == user.id).order_by(Account.created_at.desc())
    )
    return list(result.scalars().all())


async def get_account(db: AsyncSession, account_id: uuid.UUID, user: User) -> Account:
    result = await db.execute(
        select(Account).where(Account.id == account_id, Account.user_id == user.id)
    )
    account = result.scalar_one_or_none()
    if account is None:
        raise DomainError("ACCOUNT_NOT_FOUND", f"Hesap bulunamadı: {account_id}")
    return account
