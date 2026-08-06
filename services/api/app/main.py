from __future__ import annotations

from fastapi import FastAPI

from app.errors import DomainError, domain_error_handler
from app.routers.accounts import router as accounts_router
from app.routers.assets import router as assets_router
from app.routers.health import router as health_router
from app.routers.portfolio import router as portfolio_router
from app.routers.transactions import router as transactions_router

app = FastAPI(
    title="Portföy OS API",
    version="0.1.0",
    description="Kişisel portföy takip ve karar destek sistemi API'si",
)

app.add_exception_handler(DomainError, domain_error_handler)

app.include_router(health_router)
app.include_router(accounts_router)
app.include_router(assets_router)
app.include_router(transactions_router)
app.include_router(portfolio_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Portföy OS API"}
