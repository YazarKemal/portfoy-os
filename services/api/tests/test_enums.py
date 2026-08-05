from __future__ import annotations

from app.enums import DataLatency, DataSourceStatusState, TransactionType


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
