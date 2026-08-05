from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/v1/health/data-sources")
async def data_source_health() -> dict[str, object]:
    return {
        "status": "operational",
        "sources": [],
    }
