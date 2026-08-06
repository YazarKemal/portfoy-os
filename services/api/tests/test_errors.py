from __future__ import annotations

from app.errors import HTTP_STATUS_MAP, DomainError


class TestDomainError:
    def test_has_code_message_context(self) -> None:
        err = DomainError("ACCOUNT_NOT_FOUND", "Hesap bulunamadı", {"id": "123"})
        assert err.code == "ACCOUNT_NOT_FOUND"
        assert err.message == "Hesap bulunamadı"
        assert err.context == {"id": "123"}

    def test_default_context_empty(self) -> None:
        err = DomainError("ASSET_NOT_FOUND", "Varlık bulunamadı")
        assert err.context == {}

    def test_status_code_404(self) -> None:
        err = DomainError("ACCOUNT_NOT_FOUND", "x")
        assert err.status_code() == 404

    def test_status_code_422(self) -> None:
        err = DomainError("INVALID_TRANSACTION_SHAPE", "x")
        assert err.status_code() == 422

    def test_status_code_409(self) -> None:
        err = DomainError("DUPLICATE_IDEMPOTENCY_KEY", "x")
        assert err.status_code() == 409

    def test_unknown_code_500(self) -> None:
        err = DomainError("UNKNOWN_CODE", "x")
        assert err.status_code() == 500

    def test_all_required_codes_have_status(self) -> None:
        required = [
            "ACCOUNT_NOT_FOUND",
            "ASSET_NOT_FOUND",
            "TRANSACTION_NOT_FOUND",
            "INVALID_TRANSACTION_SHAPE",
            "INVALID_TRANSACTION_STATE",
            "INSUFFICIENT_CASH",
            "INSUFFICIENT_QUANTITY",
            "DUPLICATE_IDEMPOTENCY_KEY",
            "PRICE_NOT_AVAILABLE",
        ]
        for code in required:
            assert code in HTTP_STATUS_MAP, f"Missing HTTP mapping for {code}"
