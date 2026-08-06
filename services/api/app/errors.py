from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

HTTP_STATUS_MAP: dict[str, int] = {
    "ACCOUNT_NOT_FOUND": 404,
    "ASSET_NOT_FOUND": 404,
    "TRANSACTION_NOT_FOUND": 404,
    "INVALID_TRANSACTION_SHAPE": 422,
    "INVALID_TRANSACTION_STATE": 409,
    "INSUFFICIENT_CASH": 422,
    "INSUFFICIENT_QUANTITY": 422,
    "DUPLICATE_IDEMPOTENCY_KEY": 409,
    "PRICE_NOT_AVAILABLE": 422,
}


class DomainError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        context: Mapping[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.context = dict(context) if context else {}

    def status_code(self) -> int:
        return HTTP_STATUS_MAP.get(self.code, 500)


async def domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, DomainError):
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
    return JSONResponse(
        status_code=exc.status_code(),
        content={
            "detail": {
                "code": exc.code,
                "message": exc.message,
                "context": exc.context,
            }
        },
    )
