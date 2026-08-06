from __future__ import annotations

from app.enums import (
    DataLatency,
    DataSourceStatusState,
    TransactionSource,
    TransactionStatus,
    TransactionType,
)


class TestTransactionType:
    def test_all_types_present(self) -> None:
        expected = {
            "BUY", "SELL", "DEPOSIT", "WITHDRAWAL",
            "DIVIDEND", "INTEREST", "FEE", "TAX",
            "TRANSFER_IN", "TRANSFER_OUT",
        }
        actual = {t.value for t in TransactionType}
        assert actual == expected

    def test_count(self) -> None:
        assert len(TransactionType) == 10


class TestDataSourceStatusState:
    def test_states_present(self) -> None:
        expected = {"HEALTHY", "DEGRADED", "DOWN", "UNKNOWN"}
        actual = {s.value for s in DataSourceStatusState}
        assert actual == expected


class TestDataLatency:
    def test_latency_types_present(self) -> None:
        expected = {"REALTIME", "DELAYED", "END_OF_DAY", "MANUAL"}
        actual = {lat.value for lat in DataLatency}
        assert actual == expected


class TestTransactionStatus:
    def test_all_statuses_present(self) -> None:
        expected = {"DRAFT", "POSTED", "VOIDED"}
        actual = {s.value for s in TransactionStatus}
        assert actual == expected

    def test_count(self) -> None:
        assert len(TransactionStatus) == 3


class TestTransactionSource:
    def test_all_sources_present(self) -> None:
        expected = {"MANUAL", "IMPORT", "AI"}
        actual = {s.value for s in TransactionSource}
        assert actual == expected

    def test_count(self) -> None:
        assert len(TransactionSource) == 3
