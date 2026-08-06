# Portfoy OS API

Core portfolio ledger API for the Portfoy OS application.

## Single-user mode

This service operates in single-user mode. The default user is resolved via the `get_default_user` dependency, which auto-creates the configured user on first access. Real authentication can replace this dependency later without changing routers or services.

Configure the default user via environment variables:

| Variable | Default | Description |
|---|---|---|
| `DEFAULT_USER_EMAIL` | `owner@portfoy.local` | Email of the default user |
| `DEFAULT_USER_DISPLAY_NAME` | `Portfoy Sahibi` | Display name of the default user |

## Database setup

```bash
# Install dependencies
uv sync --all-groups

# Run migrations
uv run alembic upgrade head

# Verify current revision
uv run alembic current
```

## Running the server

```bash
uv run uvicorn app.main:app --reload
```

## Running tests

```bash
# All tests
uv run pytest

# Non-DB tests only
uv run pytest tests/test_enums.py tests/test_domain_money.py tests/test_domain_ledger.py tests/test_errors.py -v

# With coverage
uv run pytest --cov=app --cov-report=term-missing
```

## Lint and type checking

```bash
uv run ruff check .
uv run mypy app
```

## Example API sequence

```bash
BASE=http://localhost:8000/api/v1

# 1. Create an account
curl -s $BASE/accounts \
  -H "Content-Type: application/json" \
  -d '{"name":"Yatırım Hesabı","currency":"TRY"}' | jq

# 2. Create a deposit draft
curl -s $BASE/transactions/drafts \
  -H "Content-Type: application/json" \
  -d '{
    "account_id":"<account_id>",
    "transaction_type":"DEPOSIT",
    "gross_amount":"10000.00",
    "currency":"TRY",
    "transaction_date":"2026-01-01T12:00:00+03:00"
  }' | jq

# 3. Confirm the deposit
curl -s -X POST $BASE/transactions/<txn_id>/confirm | jq

# 4. Create an asset
curl -s $BASE/assets \
  -H "Content-Type: application/json" \
  -d '{"code":"FON1","name":"Örnek Fon","currency":"TRY"}' | jq

# 5. Add a manual price
curl -s $BASE/assets/<asset_id>/prices \
  -H "Content-Type: application/json" \
  -d '{"price":"150.00000000","market_time":"2026-01-02T12:00:00+03:00"}' | jq

# 6. Create and confirm a buy
curl -s $BASE/transactions/drafts \
  -H "Content-Type: application/json" \
  -d '{
    "account_id":"<account_id>",
    "asset_id":"<asset_id>",
    "transaction_type":"BUY",
    "quantity":"10",
    "unit_price":"150.00000000",
    "fee_amount":"5.00",
    "currency":"TRY",
    "transaction_date":"2026-01-02T12:00:00+03:00"
  }' | jq

curl -s -X POST $BASE/transactions/<txn_id>/confirm | jq

# 7. Read portfolio summary
curl -s $BASE/portfolio/summary | jq

# 8. Read holdings
curl -s $BASE/portfolio/holdings | jq
```
