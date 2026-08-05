from __future__ import annotations

from fastapi import FastAPI

from app.routers.health import router as health_router

app = FastAPI(
    title="Portföy OS API",
    version="0.1.0",
    description="Kişisel portföy takip ve karar destek sistemi API'si",
)

app.include_router(health_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Portföy OS API"}
