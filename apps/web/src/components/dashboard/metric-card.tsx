import { Card } from "@/components/ui/card";
import { formatMoney } from "@/lib/formatters";

interface MetricCardProps {
  label: string;
  value: number;
  context?: string;
  currency?: string;
  className?: string;
  masked?: boolean;
  tone?: "neutral" | "signed";
}

export function MetricCard({
  label,
  value,
  context,
  currency,
  className = "",
  masked = false,
  tone = "neutral",
}: MetricCardProps) {
  const isSigned = tone === "signed";
  const sign = isSigned ? (value > 0 ? "+" : value < 0 ? "−" : "") : "";

  const colorClass =
    masked || !isSigned
      ? "text-[var(--color-text-primary)]"
      : value > 0
        ? "text-positive"
        : value < 0
          ? "text-negative"
          : "text-[var(--color-text-primary)]";

  return (
    <Card className={className}>
      <h3 className="text-xs font-medium uppercase tracking-wide text-[var(--color-text-tertiary)] mb-2">
        {label}
      </h3>
      <p
        className={`financial-value text-xl font-semibold tabular-nums ${colorClass}`}
      >
        {masked ? "₺••••••" : `${sign}${formatMoney(Math.abs(value), currency)}`}
      </p>
      {context && (
        <p className="mt-1.5 text-xs text-[var(--color-text-tertiary)] leading-relaxed">
          {context}
        </p>
      )}
    </Card>
  );
}
