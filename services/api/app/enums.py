from __future__ import annotations

import enum


class TransactionType(enum.StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    DIVIDEND = "DIVIDEND"
    INTEREST = "INTEREST"
    FEE = "FEE"
    TAX = "TAX"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"


class DataSourceStatusState(enum.StrEnum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


class DataLatency(enum.StrEnum):
    REALTIME = "REALTIME"
    DELAYED = "DELAYED"
    END_OF_DAY = "END_OF_DAY"
    MANUAL = "MANUAL"


class TransactionStatus(enum.StrEnum):
    DRAFT = "DRAFT"
    POSTED = "POSTED"
    VOIDED = "VOIDED"


class TransactionSource(enum.StrEnum):
    MANUAL = "MANUAL"
    IMPORT = "IMPORT"
    AI = "AI"
