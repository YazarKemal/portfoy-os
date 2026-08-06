"""Core portfolio ledger

Revision ID: 002
Revises: 001
Create Date: 2026-08-06
"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create new enum types
    op.execute("CREATE TYPE transaction_status AS ENUM ('DRAFT', 'POSTED', 'VOIDED')")
    op.execute("CREATE TYPE transaction_source AS ENUM ('MANUAL', 'IMPORT', 'AI')")

    # 2. Add account columns
    op.add_column(
        "accounts",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.add_column(
        "accounts",
        sa.Column(
            "allow_negative_balance",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    # 3. Modify transactions table
    # Drop NOT NULL on asset_id, quantity, unit_price
    op.alter_column("transactions", "asset_id", nullable=True)
    op.alter_column("transactions", "quantity", nullable=True)
    op.alter_column("transactions", "unit_price", nullable=True)

    # Change unit_price precision
    op.alter_column(
        "transactions",
        "unit_price",
        type_=sa.Numeric(20, 8),
        existing_type=sa.Numeric(20, 4),
    )

    # Rename total_amount to gross_amount
    op.alter_column("transactions", "total_amount", new_column_name="gross_amount")

    # Add new financial columns
    op.add_column(
        "transactions",
        sa.Column(
            "fee_amount",
            sa.Numeric(20, 4),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "transactions",
        sa.Column(
            "tax_amount",
            sa.Numeric(20, 4),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )
    op.add_column(
        "transactions",
        sa.Column(
            "net_cash_effect",
            sa.Numeric(20, 4),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )

    # Add status and source columns
    op.add_column(
        "transactions",
        sa.Column(
            "status",
            sa.Enum("DRAFT", "POSTED", "VOIDED", name="transaction_status"),
            nullable=False,
            server_default="DRAFT",
        ),
    )
    op.add_column(
        "transactions",
        sa.Column(
            "source",
            sa.Enum("MANUAL", "IMPORT", "AI", name="transaction_source"),
            nullable=False,
            server_default="MANUAL",
        ),
    )

    # Add idempotency key
    op.add_column(
        "transactions",
        sa.Column("idempotency_key", sa.String(100), nullable=True),
    )
    op.create_unique_constraint(
        "uq_transactions_idempotency_key", "transactions", ["idempotency_key"]
    )

    # Add lifecycle columns
    op.add_column(
        "transactions",
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("voided_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column("void_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "transactions",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # 4. Add check constraints
    op.create_check_constraint(
        "chk_gross_amount_non_negative", "transactions", "gross_amount >= 0"
    )
    op.create_check_constraint(
        "chk_fee_amount_non_negative", "transactions", "fee_amount >= 0"
    )
    op.create_check_constraint(
        "chk_tax_amount_non_negative", "transactions", "tax_amount >= 0"
    )
    op.create_check_constraint(
        "chk_quantity_positive", "transactions", "quantity IS NULL OR quantity > 0"
    )
    op.create_check_constraint(
        "chk_unit_price_positive",
        "transactions",
        "unit_price IS NULL OR unit_price > 0",
    )

    # 5. Drop cash_flows table and cash_flow_type enum
    op.drop_table("cash_flows")
    op.execute("DROP TYPE IF EXISTS cash_flow_type")


def downgrade() -> None:
    # 1. Recreate cash_flow_type enum and cash_flows table
    op.execute(
        "CREATE TYPE cash_flow_type AS ENUM ("
        "'BUY', 'SELL', 'DEPOSIT', 'WITHDRAWAL', 'DIVIDEND', "
        "'INTEREST', 'FEE', 'TAX', 'TRANSFER_IN', 'TRANSFER_OUT')"
    )
    cash_flow_type_enum = postgresql.ENUM(
        "BUY",
        "SELL",
        "DEPOSIT",
        "WITHDRAWAL",
        "DIVIDEND",
        "INTEREST",
        "FEE",
        "TAX",
        "TRANSFER_IN",
        "TRANSFER_OUT",
        name="cash_flow_type",
        create_type=False,
    )
    op.create_table(
        "cash_flows",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "account_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
        sa.Column(
            "cash_flow_type",
            cash_flow_type_enum,
            nullable=False,
        ),
        sa.Column("amount", sa.Numeric(20, 4), nullable=False),
        sa.Column(
            "currency", sa.String(3), nullable=False, server_default="TRY"
        ),
        sa.Column(
            "transaction_date", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cash_flows_account_id", "cash_flows", ["account_id"])

    # 2. Drop check constraints
    op.drop_constraint("chk_unit_price_positive", "transactions")
    op.drop_constraint("chk_quantity_positive", "transactions")
    op.drop_constraint("chk_tax_amount_non_negative", "transactions")
    op.drop_constraint("chk_fee_amount_non_negative", "transactions")
    op.drop_constraint("chk_gross_amount_non_negative", "transactions")

    # 3. Remove added transaction columns (reverse order)
    op.drop_column("transactions", "updated_at")
    op.drop_column("transactions", "void_reason")
    op.drop_column("transactions", "voided_at")
    op.drop_column("transactions", "confirmed_at")
    op.drop_constraint("uq_transactions_idempotency_key", "transactions")
    op.drop_column("transactions", "idempotency_key")
    op.drop_column("transactions", "source")
    op.drop_column("transactions", "status")
    op.drop_column("transactions", "net_cash_effect")
    op.drop_column("transactions", "tax_amount")
    op.drop_column("transactions", "fee_amount")

    # 4. Rename gross_amount back to total_amount
    op.alter_column("transactions", "gross_amount", new_column_name="total_amount")

    # 5. Restore NOT NULL and original precision
    op.alter_column(
        "transactions",
        "unit_price",
        type_=sa.Numeric(20, 4),
        existing_type=sa.Numeric(20, 8),
        nullable=False,
    )
    op.alter_column("transactions", "quantity", nullable=False)
    op.alter_column("transactions", "asset_id", nullable=False)

    # 6. Remove account columns
    op.drop_column("accounts", "allow_negative_balance")
    op.drop_column("accounts", "is_active")

    # 7. Drop new enum types
    op.execute("DROP TYPE IF EXISTS transaction_source")
    op.execute("DROP TYPE IF EXISTS transaction_status")
