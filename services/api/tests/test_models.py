from __future__ import annotations

import uuid
from datetime import UTC, datetime
from decimal import Decimal

from app.enums import DataLatency, DataSourceStatusState, TransactionType
from app.models import (
    Account,
    Asset,
    AssetPrice,
    CashFlow,
    DataSourceStatus,
    PortfolioSnapshot,
    Transaction,
    User,
)


class TestUserModel:
    def test_create_minimal(self) -> None:
        user = User(email="test@example.com", display_name="Test User")
        assert user.email == "test@example.com"
        assert user.display_name == "Test User"
        assert isinstance(user.id, uuid.UUID)

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
        """Money fields must use Decimal, not float."""
        price = AssetPrice(
            asset_id=uuid.uuid4(),
            price=Decimal("100.5000"),
            provider="test",
            market_time=datetime.now(UTC),
            data_latency=DataLatency.MANUAL,
        )
        assert isinstance(price.price, Decimal)


class TestTransactionModel:
    def test_create_buy(self) -> None:
        txn = Transaction(
            account_id=uuid.uuid4(),
            asset_id=uuid.uuid4(),
            transaction_type=TransactionType.BUY,
            quantity=Decimal("10"),
            unit_price=Decimal("100.0000"),
            total_amount=Decimal("1000.0000"),
            transaction_date=datetime.now(UTC),
        )
        assert txn.transaction_type == TransactionType.BUY

    def test_amount_fields_are_decimal(self) -> None:
        txn = Transaction(
            account_id=uuid.uuid4(),
            asset_id=uuid.uuid4(),
            transaction_type=TransactionType.BUY,
            quantity=Decimal("10"),
            unit_price=Decimal("100.0000"),
            total_amount=Decimal("1000.0000"),
            transaction_date=datetime.now(UTC),
        )
        assert isinstance(txn.quantity, Decimal)
        assert isinstance(txn.unit_price, Decimal)
        assert isinstance(txn.total_amount, Decimal)


class TestCashFlowModel:
    def test_create_cash_flow(self) -> None:
        cf = CashFlow(
            account_id=uuid.uuid4(),
            cash_flow_type=TransactionType.DIVIDEND,
            amount=Decimal("50.0000"),
            transaction_date=datetime.now(UTC),
        )
        assert cf.cash_flow_type == TransactionType.DIVIDEND
        assert cf.amount == Decimal("50.0000")
        assert isinstance(cf.amount, Decimal)


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
    def test_create_default(self) -> None:
        status = DataSourceStatus(provider="tefas")
        assert status.provider == "tefas"
        assert status.status == DataSourceStatusState.UNKNOWN
