from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ledger import (
    AccountState,
    LedgerEvent,
    Position,
    project_state,
    run_ledger,
)
from app.domain.money import (
    quantize_money,
    quantize_price,
    quantize_quantity,
    require_non_negative,
    require_positive,
)
from app.enums import TransactionSource, TransactionStatus, TransactionType
from app.errors import DomainError
from app.models import Account, Asset, Transaction, User

ASSET_REQUIRED_TYPES = {TransactionType.BUY, TransactionType.SELL, TransactionType.DIVIDEND}
ASSET_FORBIDDEN_TYPES = {
    TransactionType.DEPOSIT,
    TransactionType.WITHDRAWAL,
    TransactionType.TRANSFER_IN,
    TransactionType.TRANSFER_OUT,
}
CASH_EVENT_TYPES = {
    TransactionType.DIVIDEND,
    TransactionType.INTEREST,
    TransactionType.DEPOSIT,
    TransactionType.WITHDRAWAL,
    TransactionType.FEE,
    TransactionType.TAX,
    TransactionType.TRANSFER_IN,
    TransactionType.TRANSFER_OUT,
}
TRADE_TYPES = {TransactionType.BUY, TransactionType.SELL}


def _to_ledger_event(txn: Transaction) -> LedgerEvent:
    return LedgerEvent(
        id=txn.id,
        account_id=txn.account_id,
        asset_id=txn.asset_id,
        transaction_type=txn.transaction_type,
        quantity=txn.quantity or Decimal("0"),
        unit_price=txn.unit_price or Decimal("0"),
        gross_amount=txn.gross_amount,
        fee_amount=txn.fee_amount,
        tax_amount=txn.tax_amount,
        net_cash_effect=txn.net_cash_effect,
        transaction_date=txn.transaction_date,
        created_at=txn.created_at,
    )


async def _compute_current_state(
    db: AsyncSession, account_id: uuid.UUID
) -> AccountState:
    result = await db.execute(
        select(Transaction)
        .where(
            Transaction.account_id == account_id,
            Transaction.status == TransactionStatus.POSTED,
        )
        .order_by(
            Transaction.transaction_date,
            Transaction.created_at,
            Transaction.id,
        )
    )
    posted = result.scalars().all()
    events = [_to_ledger_event(t) for t in posted]
    states = run_ledger(events)
    return states.get(account_id, AccountState())


def _derive_gross_amount(
    transaction_type: TransactionType,
    quantity: Decimal | None,
    unit_price: Decimal | None,
    gross_amount: Decimal | None,
) -> Decimal:
    if transaction_type in TRADE_TYPES:
        if quantity is None or unit_price is None:
            raise DomainError(
                "INVALID_TRANSACTION_SHAPE",
                "Alım/satım işlemlerinde miktar ve birim fiyat zorunludur.",
            )
        derived = quantize_money(quantity * unit_price)
        if gross_amount is not None and quantize_money(gross_amount) != derived:
            raise DomainError(
                "INVALID_TRANSACTION_SHAPE",
                f"Brüt tutar uyuşmazlığı: hesaplanan={derived}, gönderilen={gross_amount}",
            )
        return derived

    if gross_amount is None:
        raise DomainError(
            "INVALID_TRANSACTION_SHAPE",
            "Nakit işlemlerde brüt tutar zorunludur.",
        )
    return require_positive(quantize_money(gross_amount), "gross_amount")


def _derive_cash_effect(
    transaction_type: TransactionType,
    quantity: Decimal | None,
    unit_price: Decimal | None,
    gross_amount: Decimal,
    fee_amount: Decimal,
    tax_amount: Decimal,
) -> Decimal:
    if transaction_type == TransactionType.BUY:
        gross = quantity * unit_price  # type: ignore[operator]
        return quantize_money(-(gross + fee_amount + tax_amount))
    elif transaction_type == TransactionType.SELL:
        gross = quantity * unit_price  # type: ignore[operator]
        return quantize_money(gross - fee_amount - tax_amount)
    elif transaction_type in (TransactionType.DIVIDEND, TransactionType.INTEREST):
        return quantize_money(gross_amount - fee_amount - tax_amount)
    elif transaction_type == TransactionType.DEPOSIT:
        return quantize_money(gross_amount)
    elif transaction_type in (
        TransactionType.WITHDRAWAL,
        TransactionType.FEE,
        TransactionType.TAX,
    ):
        return quantize_money(-gross_amount)
    elif transaction_type == TransactionType.TRANSFER_IN:
        return quantize_money(gross_amount)
    elif transaction_type == TransactionType.TRANSFER_OUT:
        return quantize_money(-gross_amount)
    raise DomainError("INVALID_TRANSACTION_SHAPE", f"Bilinmeyen işlem türü: {transaction_type}")


async def create_draft(
    db: AsyncSession,
    user: User,
    *,
    account_id: uuid.UUID,
    asset_id: uuid.UUID | None,
    transaction_type: TransactionType,
    quantity: Decimal | None,
    unit_price: Decimal | None,
    gross_amount: Decimal | None,
    fee_amount: Decimal,
    tax_amount: Decimal,
    currency: str,
    transaction_date: datetime,
    source: TransactionSource,
    idempotency_key: str | None,
    notes: str | None,
) -> tuple[Transaction, AccountState, AccountState, list[str]]:
    # Normalize inputs
    currency = currency.upper()
    fee_amount = require_non_negative(quantize_money(fee_amount), "fee_amount")
    tax_amount = require_non_negative(quantize_money(tax_amount), "tax_amount")

    if transaction_date.tzinfo is None:
        raise DomainError(
            "INVALID_TRANSACTION_SHAPE",
            "İşlem tarihi zaman dilimi bilgisi içermelidir.",
        )

    # Validate asset rules
    if transaction_type in ASSET_REQUIRED_TYPES:
        if asset_id is None:
            raise DomainError(
                "INVALID_TRANSACTION_SHAPE",
                f"{transaction_type.value} işleminde varlık zorunludur.",
            )
    elif transaction_type in ASSET_FORBIDDEN_TYPES and asset_id is not None:
        raise DomainError(
            "INVALID_TRANSACTION_SHAPE",
            f"{transaction_type.value} işleminde varlık belirtilemez.",
        )

    # Verify account
    account_result = await db.execute(
        select(Account).where(Account.id == account_id, Account.user_id == user.id)
    )
    account = account_result.scalar_one_or_none()
    if account is None:
        raise DomainError("ACCOUNT_NOT_FOUND", f"Hesap bulunamadı: {account_id}")
    if not account.is_active:
        raise DomainError("INVALID_TRANSACTION_SHAPE", "Hesap aktif değil.")

    # Verify asset if provided
    if asset_id is not None:
        asset_result = await db.execute(select(Asset).where(Asset.id == asset_id))
        if asset_result.scalar_one_or_none() is None:
            raise DomainError("ASSET_NOT_FOUND", f"Varlık bulunamadı: {asset_id}")

    # Normalize quantity and unit_price
    if quantity is not None:
        quantity = require_positive(quantize_quantity(quantity), "quantity")
    if unit_price is not None:
        unit_price = require_positive(quantize_price(unit_price), "unit_price")

    # Derive gross_amount
    derived_gross = _derive_gross_amount(
        transaction_type, quantity, unit_price, gross_amount
    )

    # Derive cash effect
    net_cash_effect = _derive_cash_effect(
        transaction_type, quantity, unit_price, derived_gross, fee_amount, tax_amount
    )

    # Idempotency check
    if idempotency_key is not None:
        existing = await db.execute(
            select(Transaction).where(
                Transaction.idempotency_key == idempotency_key
            )
        )
        existing_txn = existing.scalar_one_or_none()
        if existing_txn is not None:
            if (
                existing_txn.account_id == account_id
                and existing_txn.transaction_type == transaction_type
                and existing_txn.gross_amount == derived_gross
                and existing_txn.fee_amount == fee_amount
                and existing_txn.tax_amount == tax_amount
            ):
                current = await _compute_current_state(db, account_id)
                projected = project_state(
                    current,
                    transaction_type,
                    asset_id,
                    quantity,
                    derived_gross,
                    fee_amount,
                    tax_amount,
                    net_cash_effect,
                )
                return existing_txn, current, projected, []
            raise DomainError(
                "DUPLICATE_IDEMPOTENCY_KEY",
                f"Aynı idempotency anahtarı farklı bir işlemle kullanılmış: {idempotency_key}",
            )

    # Compute current and projected states
    current_state = await _compute_current_state(db, account_id)
    projected = project_state(
        current_state,
        transaction_type,
        asset_id,
        quantity,
        derived_gross,
        fee_amount,
        tax_amount,
        net_cash_effect,
    )

    warnings: list[str] = []

    # Check quantity for sells
    if transaction_type == TransactionType.SELL and asset_id is not None:
        pos = current_state.positions.get(asset_id, Position())
        if quantity is not None and quantity > pos.quantity:
            raise DomainError(
                "INSUFFICIENT_QUANTITY",
                f"Yetersiz varlık: mevcut={pos.quantity}, satılmak istenen={quantity}",
            )

    # Check cash
    if projected.cash_balance < 0 and not account.allow_negative_balance:
        raise DomainError(
            "INSUFFICIENT_CASH",
            f"Yetersiz nakit: bakiye={current_state.cash_balance}, "
            f"işlem sonrası={projected.cash_balance}",
        )

    if projected.cash_balance < 0 and account.allow_negative_balance:
        warnings.append("Bakiye negatife düşecek.")

    # Persist draft
    txn = Transaction(
        account_id=account_id,
        asset_id=asset_id,
        transaction_type=transaction_type,
        quantity=quantity,
        unit_price=unit_price,
        gross_amount=derived_gross,
        fee_amount=fee_amount,
        tax_amount=tax_amount,
        net_cash_effect=net_cash_effect,
        currency=currency,
        status=TransactionStatus.DRAFT,
        source=source,
        idempotency_key=idempotency_key,
        transaction_date=transaction_date,
        notes=notes,
    )
    db.add(txn)
    try:
        await db.flush()
    except Exception:
        await db.rollback()
        # Check again for race on idempotency_key
        if idempotency_key is not None:
            existing = await db.execute(
                select(Transaction).where(
                    Transaction.idempotency_key == idempotency_key
                )
            )
            existing_txn = existing.scalar_one_or_none()
            if existing_txn is not None:
                raise DomainError(
                    "DUPLICATE_IDEMPOTENCY_KEY",
                    f"Bu idempotency anahtarı zaten kullanılmış: {idempotency_key}",
                ) from None
        raise

    await db.refresh(txn)
    return txn, current_state, projected, warnings


async def list_transactions(
    db: AsyncSession,
    user: User,
    *,
    account_id: uuid.UUID | None = None,
    asset_id: uuid.UUID | None = None,
    transaction_type: TransactionType | None = None,
    status: TransactionStatus | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[Transaction], int]:
    if limit < 1 or limit > 200:
        limit = 50

    # Get user's account IDs
    from sqlalchemy import func as sqlfunc

    account_ids_query = select(Account.id).where(Account.user_id == user.id)
    account_ids_result = await db.execute(account_ids_query)
    user_account_ids = [row[0] for row in account_ids_result.all()]

    if not user_account_ids:
        return [], 0

    from sqlalchemy.sql.elements import ColumnElement

    conditions: list[ColumnElement[bool]] = [
        Transaction.account_id.in_(user_account_ids)
    ]

    if account_id is not None:
        if account_id not in user_account_ids:
            return [], 0
        conditions.append(Transaction.account_id == account_id)
    if asset_id is not None:
        conditions.append(Transaction.asset_id == asset_id)
    if transaction_type is not None:
        conditions.append(Transaction.transaction_type == transaction_type)
    if status is not None:
        conditions.append(Transaction.status == status)

    count_query = select(sqlfunc.count()).select_from(Transaction).where(*conditions)
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    query = (
        select(Transaction)
        .where(*conditions)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(query)
    transactions = list(result.scalars().all())

    return transactions, total


async def get_transaction(
    db: AsyncSession, transaction_id: uuid.UUID, user: User
) -> Transaction:
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id)
    )
    txn = result.scalar_one_or_none()
    if txn is None:
        raise DomainError("TRANSACTION_NOT_FOUND", f"İşlem bulunamadı: {transaction_id}")

    # Verify ownership
    account_result = await db.execute(
        select(Account).where(Account.id == txn.account_id, Account.user_id == user.id)
    )
    if account_result.scalar_one_or_none() is None:
        raise DomainError("TRANSACTION_NOT_FOUND", f"İşlem bulunamadı: {transaction_id}")

    return txn


async def confirm_transaction(
    db: AsyncSession, transaction_id: uuid.UUID, user: User
) -> Transaction:
    # Lock the transaction row
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id)
        .with_for_update()
    )
    txn = result.scalar_one_or_none()
    if txn is None:
        raise DomainError("TRANSACTION_NOT_FOUND", f"İşlem bulunamadı: {transaction_id}")

    # Verify ownership
    account_result = await db.execute(
        select(Account).where(Account.id == txn.account_id, Account.user_id == user.id)
    )
    account = account_result.scalar_one_or_none()
    if account is None:
        raise DomainError("TRANSACTION_NOT_FOUND", f"İşlem bulunamadı: {transaction_id}")

    if txn.status != TransactionStatus.DRAFT:
        raise DomainError(
            "INVALID_TRANSACTION_STATE",
            f"Sadece DRAFT işlemler onaylanabilir. Mevcut durum: {txn.status.value}",
        )

    # Lock account for cash check
    await db.execute(
        select(Account).where(Account.id == txn.account_id).with_for_update()
    )

    # Recompute current state and validate
    current_state = await _compute_current_state(db, txn.account_id)

    projected = project_state(
        current_state,
        txn.transaction_type,
        txn.asset_id,
        txn.quantity,
        txn.gross_amount,
        txn.fee_amount,
        txn.tax_amount,
        txn.net_cash_effect,
    )

    # Check quantity for sells
    if txn.transaction_type == TransactionType.SELL and txn.asset_id is not None:
        pos = current_state.positions.get(txn.asset_id, Position())
        if txn.quantity is not None and txn.quantity > pos.quantity:
            raise DomainError(
                "INSUFFICIENT_QUANTITY",
                f"Yetersiz varlık: mevcut={pos.quantity}, satılmak istenen={txn.quantity}",
            )

    if projected.cash_balance < 0 and not account.allow_negative_balance:
        raise DomainError(
            "INSUFFICIENT_CASH",
            f"Yetersiz nakit: bakiye={current_state.cash_balance}, "
            f"işlem sonrası={projected.cash_balance}",
        )

    txn.status = TransactionStatus.POSTED
    txn.confirmed_at = datetime.now(UTC)
    await db.flush()
    await db.refresh(txn)
    return txn


async def void_transaction(
    db: AsyncSession, transaction_id: uuid.UUID, reason: str, user: User
) -> Transaction:
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id)
        .with_for_update()
    )
    txn = result.scalar_one_or_none()
    if txn is None:
        raise DomainError("TRANSACTION_NOT_FOUND", f"İşlem bulunamadı: {transaction_id}")

    # Verify ownership
    account_result = await db.execute(
        select(Account).where(Account.id == txn.account_id, Account.user_id == user.id)
    )
    if account_result.scalar_one_or_none() is None:
        raise DomainError("TRANSACTION_NOT_FOUND", f"İşlem bulunamadı: {transaction_id}")

    if txn.status != TransactionStatus.DRAFT:
        raise DomainError(
            "INVALID_TRANSACTION_STATE",
            f"Sadece DRAFT işlemler iptal edilebilir. Mevcut durum: {txn.status.value}",
        )

    if not reason.strip():
        raise DomainError("INVALID_TRANSACTION_SHAPE", "İptal sebebi boş olamaz.")

    txn.status = TransactionStatus.VOIDED
    txn.voided_at = datetime.now(UTC)
    txn.void_reason = reason.strip()
    await db.flush()
    await db.refresh(txn)
    return txn
