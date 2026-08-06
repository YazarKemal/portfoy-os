from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from app.database import async_session_factory
from app.enums import (
    DataLatency,
    DataSourceStatusState,
    TransactionSource,
    TransactionStatus,
    TransactionType,
)
from app.models import (
    Account,
    Asset,
    AssetPrice,
    DataSourceStatus,
    PortfolioSnapshot,
    Transaction,
    User,
)


class TestUserModel:
    async def test_create_minimal(self) -> None:
        user = User(
            email="test@example.com",
            display_name="Test User",
        )

        async with async_session_factory() as session:
            session.add(user)
            await session.flush()

            assert user.email == "test@example.com"
            assert user.display_name == "Test User"
            assert isinstance(user.id, uuid.UUID)

            await session.rollback()

    def test_email_unique(self) -> None:
        assert hasattr(User, "email")
        assert getattr(User.email, "unique", False) or getattr(
            getattr(User.email, "property", None), "columns", [None]
        )[0].unique


class TestAccountModel:
    def test_create_minimal(self) -> None:
        account = Account(
            user_id=uuid.uuid4(),
            name="Test Account",
            currency="TRY",
        )
        assert account.name == "Test Account"
        assert account.currency == "TRY"
        assert account.is_active is True
        assert account.allow_negative_balance is False


class TestAssetModel:
    def test_create_minimal(self) -> None:
        asset = Asset(code="TEST", name="Test Asset", asset_type="stock")
        assert asset.code == "TEST"
        assert asset.asset_type == "stock"


class TestAssetPriceModel:
    def test_create_minimal(self) -> None:
        now = datetime.now(UTC)
        price = AssetPrice(
            asset_id=uuid.uuid4(),
            price=Decimal("100.5000"),
            provider="manual",
            market_time=now,
            data_latency=DataLatency.MANUAL,
        )
        assert price.price == Decimal("100.5000")
        assert price.provider == "manual"
        assert price.data_latency == DataLatency.MANUAL

    def test_price_is_numeric_not_float(self) -> None:
        price = AssetPrice(
            asset_id=uuid.uuid4(),
            price=Decimal("100.5000"),
            provider="test",
            market_time=datetime.now(UTC),
            data_latency=DataLatency.MANUAL,
        )
        assert isinstance(price.price, Decimal)


class TestTransactionModel:
    def test_create_buy_draft(self) -> None:
        txn = Transaction(
            account_id=uuid.uuid4(),
            asset_id=uuid.uuid4(),
            transaction_type=TransactionType.BUY,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
            gross_amount=Decimal("1000.0000"),
            fee_amount=Decimal("0"),
            tax_amount=Decimal("0"),
            net_cash_effect=Decimal("-1000.0000"),
            status=TransactionStatus.DRAFT,
            source=TransactionSource.MANUAL,
            transaction_date=datetime.now(UTC),
        )
        assert txn.transaction_type == TransactionType.BUY
        assert txn.status == TransactionStatus.DRAFT
        assert txn.source == TransactionSource.MANUAL

    def test_amount_fields_are_decimal(self) -> None:
        txn = Transaction(
            account_id=uuid.uuid4(),
            asset_id=uuid.uuid4(),
            transaction_type=TransactionType.BUY,
            quantity=Decimal("10"),
            unit_price=Decimal("100.00000000"),
            gross_amount=Decimal("1000.0000"),
            fee_amount=Decimal("0"),
            tax_amount=Decimal("0"),
            net_cash_effect=Decimal("-1000.0000"),
            status=TransactionStatus.DRAFT,
            source=TransactionSource.MANUAL,
            transaction_date=datetime.now(UTC),
        )
        assert isinstance(txn.quantity, Decimal)
        assert isinstance(txn.unit_price, Decimal)
        assert isinstance(txn.gross_amount, Decimal)
        assert isinstance(txn.fee_amount, Decimal)
        assert isinstance(txn.tax_amount, Decimal)
        assert isinstance(txn.net_cash_effect, Decimal)

    def test_defaults(self) -> None:
        txn = Transaction(
            account_id=uuid.uuid4(),
            transaction_type=TransactionType.DEPOSIT,
            gross_amount=Decimal("100.0000"),
            net_cash_effect=Decimal("100.0000"),
            transaction_date=datetime.now(UTC),
        )
        assert txn.status == TransactionStatus.DRAFT
        assert txn.source == TransactionSource.MANUAL
        assert txn.fee_amount == Decimal("0")
        assert txn.tax_amount == Decimal("0")
        assert txn.asset_id is None

    def test_cash_event_nullable_asset(self) -> None:
        txn = Transaction(
            account_id=uuid.uuid4(),
            asset_id=None,
            transaction_type=TransactionType.DEPOSIT,
            quantity=None,
            unit_price=None,
            gross_amount=Decimal("500.0000"),
            net_cash_effect=Decimal("500.0000"),
            transaction_date=datetime.now(UTC),
        )
        assert txn.asset_id is None
        assert txn.quantity is None
        assert txn.unit_price is None


class TestPortfolioSnapshotModel:
    def test_create_snapshot(self) -> None:
        snap = PortfolioSnapshot(
            user_id=uuid.uuid4(),
            snapshot_date=datetime.now(UTC),
            total_value=Decimal("100000.0000"),
        )
        assert snap.total_value == Decimal("100000.0000")
        assert isinstance(snap.total_value, Decimal)


class TestDataSourceStatusModel:
    async def test_create_default(self) -> None:
        status = DataSourceStatus(provider="tefas")

        async with async_session_factory() as session:
            session.add(status)
            await session.flush()

            assert status.provider == "tefas"
            assert status.status == DataSourceStatusState.UNKNOWN
            assert isinstance(status.id, uuid.UUID)

            await session.rollback()
