from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)  # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


def _now() -> str:
    return datetime.now(UTC).isoformat()


# ── Health ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── Accounts ────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_account(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/accounts",
        json={"name": "Test Account", "currency": "TRY"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Account"
    assert data["currency"] == "TRY"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_list_accounts(client: AsyncClient) -> None:
    response = await client.get("/api/v1/accounts")
    assert response.status_code == 200
    data = response.json()
    assert "accounts" in data
    assert "count" in data


@pytest.mark.asyncio
async def test_get_account(client: AsyncClient) -> None:
    # Create first
    create_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Get Test", "currency": "TRY"},
    )
    account_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/accounts/{account_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Get Test"


@pytest.mark.asyncio
async def test_get_account_not_found(client: AsyncClient) -> None:
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/accounts/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "ACCOUNT_NOT_FOUND"


# ── Assets ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_asset(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/assets",
        json={"code": "FON001", "name": "Test Fund", "asset_type": "mutual_fund"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "FON001"
    assert data["name"] == "Test Fund"


@pytest.mark.asyncio
async def test_list_assets(client: AsyncClient) -> None:
    response = await client.get("/api/v1/assets")
    assert response.status_code == 200
    data = response.json()
    assert "assets" in data


@pytest.mark.asyncio
async def test_add_and_get_latest_price(client: AsyncClient) -> None:
    # Create asset
    asset_resp = await client.post(
        "/api/v1/assets",
        json={"code": "PRICE001", "name": "Price Test", "asset_type": "stock"},
    )
    asset_id = asset_resp.json()["id"]

    # Add first price
    t1 = datetime(2026, 1, 15, tzinfo=UTC).isoformat()
    await client.post(
        f"/api/v1/assets/{asset_id}/prices",
        json={"price": "100.0000", "currency": "TRY", "market_time": t1},
    )

    # Add second (newer) price
    t2 = datetime(2026, 1, 16, tzinfo=UTC).isoformat()
    await client.post(
        f"/api/v1/assets/{asset_id}/prices",
        json={"price": "110.0000", "currency": "TRY", "market_time": t2},
    )

    # Latest should be the second
    response = await client.get(f"/api/v1/assets/{asset_id}/prices/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == "110.0000"
    assert data["provider"] == "manual"


# ── Transactions ────────────────────────────────────────────


@pytest.mark.asyncio
async def test_deposit_draft_does_not_affect_portfolio(client: AsyncClient) -> None:
    # Create account
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Deposit Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    # Create draft
    draft_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "1000.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    assert draft_resp.status_code == 201
    assert draft_resp.json()["status"] == "DRAFT"

    # Portfolio should show 0
    summary = await client.get("/api/v1/portfolio/summary")
    assert summary.status_code == 200
    assert summary.json()["cash_balance"] == "0.0000"


@pytest.mark.asyncio
async def test_deposit_confirm_affects_cash(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Confirm Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    draft_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "1000.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    txn_id = draft_resp.json()["id"]

    # Confirm
    confirm_resp = await client.post(f"/api/v1/transactions/{txn_id}/confirm")
    assert confirm_resp.status_code == 200
    assert confirm_resp.json()["status"] == "POSTED"

    # Check portfolio
    summary = await client.get("/api/v1/portfolio/summary")
    assert summary.json()["cash_balance"] == "1000.0000"
    assert summary.json()["net_external_contributions"] == "1000.0000"


@pytest.mark.asyncio
async def test_buy_insufficient_cash(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "No Cash", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    asset_resp = await client.post(
        "/api/v1/assets",
        json={"code": "BUYTEST", "name": "Buy Test", "asset_type": "stock"},
    )
    asset_id = asset_resp.json()["id"]

    response = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "asset_id": asset_id,
            "transaction_type": "BUY",
            "quantity": "10",
            "unit_price": "100.00000000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INSUFFICIENT_CASH"


@pytest.mark.asyncio
async def test_buy_and_confirm_after_deposit(client: AsyncClient) -> None:
    # Create account, asset
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Buy Flow", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    asset_resp = await client.post(
        "/api/v1/assets",
        json={"code": "FULLFLOW", "name": "Full Flow", "asset_type": "stock"},
    )
    asset_id = asset_resp.json()["id"]

    # Deposit
    d_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "2000.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    await client.post(f"/api/v1/transactions/{d_resp.json()['id']}/confirm")

    # Buy
    buy_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "asset_id": asset_id,
            "transaction_type": "BUY",
            "quantity": "10",
            "unit_price": "100.00000000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    assert buy_resp.status_code == 201
    buy_id = buy_resp.json()["id"]

    # Confirm buy
    confirm_resp = await client.post(f"/api/v1/transactions/{buy_id}/confirm")
    assert confirm_resp.status_code == 200

    # Check summary
    summary = await client.get("/api/v1/portfolio/summary")
    assert summary.json()["cash_balance"] == "1000.0000"
    assert summary.json()["open_position_count"] == 1


@pytest.mark.asyncio
async def test_sell_insufficient_quantity(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Sell Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    asset_resp = await client.post(
        "/api/v1/assets",
        json={"code": "SELLTEST", "name": "Sell Test", "asset_type": "stock"},
    )
    asset_id = asset_resp.json()["id"]

    # Try to sell without having any
    response = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "asset_id": asset_id,
            "transaction_type": "SELL",
            "quantity": "10",
            "unit_price": "100.00000000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INSUFFICIENT_QUANTITY"


@pytest.mark.asyncio
async def test_idempotency_equivalent_request(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Idem Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    payload = {
        "account_id": account_id,
        "transaction_type": "DEPOSIT",
        "gross_amount": "500.0000",
        "currency": "TRY",
        "transaction_date": _now(),
        "idempotency_key": "idem-001",
    }

    first = await client.post("/api/v1/transactions/drafts", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/v1/transactions/drafts", json=payload)
    assert second.status_code == 201
    assert second.json()["id"] == first.json()["id"]


@pytest.mark.asyncio
async def test_idempotency_conflicting_request(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Idem Conflict", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    payload1 = {
        "account_id": account_id,
        "transaction_type": "DEPOSIT",
        "gross_amount": "500.0000",
        "currency": "TRY",
        "transaction_date": _now(),
        "idempotency_key": "idem-conflict-001",
    }

    await client.post("/api/v1/transactions/drafts", json=payload1)

    # Same key, different amount
    payload2 = {**payload1, "gross_amount": "999.0000"}
    response = await client.post("/api/v1/transactions/drafts", json=payload2)
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "DUPLICATE_IDEMPOTENCY_KEY"


@pytest.mark.asyncio
async def test_void_draft(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Void Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    draft_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "100.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    txn_id = draft_resp.json()["id"]

    void_resp = await client.post(
        f"/api/v1/transactions/{txn_id}/void",
        json={"reason": "Test cancellation"},
    )
    assert void_resp.status_code == 200
    assert void_resp.json()["status"] == "VOIDED"
    assert void_resp.json()["void_reason"] == "Test cancellation"


@pytest.mark.asyncio
async def test_posted_cannot_be_voided(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "No Void Posted", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    draft_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "100.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    txn_id = draft_resp.json()["id"]
    await client.post(f"/api/v1/transactions/{txn_id}/confirm")

    void_resp = await client.post(
        f"/api/v1/transactions/{txn_id}/void",
        json={"reason": "Attempt void of posted"},
    )
    assert void_resp.status_code == 409


@pytest.mark.asyncio
async def test_transaction_filters(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Filter Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    # Create a deposit
    await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "100.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )

    # List by type
    response = await client.get(
        f"/api/v1/transactions?transaction_type=DEPOSIT&account_id={account_id}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1

    # List by status
    response = await client.get(
        f"/api/v1/transactions?status=DRAFT&account_id={account_id}"
    )
    assert response.status_code == 200


# ── Portfolio ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_summary_with_valued_position(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Portfolio Test", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    asset_resp = await client.post(
        "/api/v1/assets",
        json={"code": "PORTTEST", "name": "Portfolio Asset", "asset_type": "stock"},
    )
    asset_id = asset_resp.json()["id"]

    # Deposit + confirm
    d_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "2000.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    await client.post(f"/api/v1/transactions/{d_resp.json()['id']}/confirm")

    # Buy + confirm
    b_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "asset_id": asset_id,
            "transaction_type": "BUY",
            "quantity": "10",
            "unit_price": "100.00000000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    await client.post(f"/api/v1/transactions/{b_resp.json()['id']}/confirm")

    # Add price
    t = datetime(2026, 1, 16, tzinfo=UTC).isoformat()
    await client.post(
        f"/api/v1/assets/{asset_id}/prices",
        json={"price": "110.0000", "currency": "TRY", "market_time": t},
    )

    summary = await client.get("/api/v1/portfolio/summary")
    assert summary.status_code == 200
    s = summary.json()
    assert s["open_position_count"] == 1
    assert s["total_market_value"] is not None
    assert s["unrealized_pnl"] is not None

    holdings = await client.get("/api/v1/portfolio/holdings")
    assert holdings.status_code == 200
    h = holdings.json()
    assert h["count"] == 1
    assert h["holdings"][0]["valuation_status"] == "VALUED"


@pytest.mark.asyncio
async def test_summary_missing_price_null_totals(client: AsyncClient) -> None:
    acc_resp = await client.post(
        "/api/v1/accounts",
        json={"name": "Missing Price", "currency": "TRY"},
    )
    account_id = acc_resp.json()["id"]

    asset_resp = await client.post(
        "/api/v1/assets",
        json={"code": "NOPRICE", "name": "No Price Asset", "asset_type": "stock"},
    )
    asset_id = asset_resp.json()["id"]

    # Deposit + confirm
    d_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "transaction_type": "DEPOSIT",
            "gross_amount": "2000.0000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    await client.post(f"/api/v1/transactions/{d_resp.json()['id']}/confirm")

    # Buy + confirm (no price added)
    b_resp = await client.post(
        "/api/v1/transactions/drafts",
        json={
            "account_id": account_id,
            "asset_id": asset_id,
            "transaction_type": "BUY",
            "quantity": "10",
            "unit_price": "100.00000000",
            "currency": "TRY",
            "transaction_date": _now(),
        },
    )
    await client.post(f"/api/v1/transactions/{b_resp.json()['id']}/confirm")

    summary = await client.get("/api/v1/portfolio/summary")
    assert summary.status_code == 200
    s = summary.json()
    assert s["cash_balance"] == "1000.0000"
    assert s["open_position_count"] == 1
    assert s["missing_price_count"] == 1
    assert s["total_market_value"] is None
    assert s["unrealized_pnl"] is None
    assert s["total_portfolio_value"] is None

    holdings = await client.get("/api/v1/portfolio/holdings")
    h = holdings.json()
    assert h["holdings"][0]["valuation_status"] == "PRICE_MISSING"
