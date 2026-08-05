/** tr-TR formatting utilities — no financial calculations. */

const TRY_FORMATTER = new Intl.NumberFormat("tr-TR", {
  style: "currency",
  currency: "TRY",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const USD_FORMATTER = new Intl.NumberFormat("tr-TR", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const PERCENT_FORMATTER = new Intl.NumberFormat("tr-TR", {
  style: "percent",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const PERCENT_COMPACT = new Intl.NumberFormat("tr-TR", {
  style: "percent",
  minimumFractionDigits: 0,
  maximumFractionDigits: 1,
});

const NUMBER_FORMATTER = new Intl.NumberFormat("tr-TR", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

const QUANTITY_FORMATTER = new Intl.NumberFormat("tr-TR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 10,
});

export function formatMoney(
  value: number,
  currency?: string,
): string {
  if (currency === "USD") {
    return USD_FORMATTER.format(value);
  }
  return TRY_FORMATTER.format(value);
}

export function formatMoneyMasked(): string {
  return "₺••••••••";
}

export function formatPercent(value: number, compact?: boolean): string {
  const pct = value / 100;
  return compact ? PERCENT_COMPACT.format(pct) : PERCENT_FORMATTER.format(pct);
}

export function formatChange(
  value: number,
  percent: number,
  currency?: string,
): { amount: string; percentStr: string; sign: string } {
  const sign = value > 0 ? "+" : value < 0 ? "−" : "";
  return {
    amount: `${sign}${formatMoney(Math.abs(value), currency)}`,
    percentStr: `${sign}${formatPercent(Math.abs(percent))}`,
    sign,
  };
}

export function formatNumber(value: number): string {
  return NUMBER_FORMATTER.format(value);
}

export function formatQuantity(value: number): string {
  return QUANTITY_FORMATTER.format(value);
}

export function formatDate(dateStr: string): string {
  const d = new Date(dateStr);
  return new Intl.DateTimeFormat("tr-TR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(d);
}

export function formatDateTime(dateTimeStr: string): string {
  const d = new Date(dateTimeStr);
  return new Intl.DateTimeFormat("tr-TR", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(d);
}

/** Returns sign indicator: "+", "−", or "" */
export function getSign(value: number): string {
  return value > 0 ? "+" : value < 0 ? "−" : "";
}

/** Returns the CSS class for positive/negative colour */
export function changeColorClass(value: number): string {
  if (value > 0) return "text-positive";
  if (value < 0) return "text-negative";
  return "";
}
