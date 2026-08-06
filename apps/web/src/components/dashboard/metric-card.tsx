import { Card } from "@/components/ui/card";
import { formatMoney, getSign } from "@/lib/formatters";

interface MetricCardProps {
  label: string;
  value: number;
  context?: string;
  currency?: string;
  className?: string;
  masked?: boolean;
}

export function MetricCard({
  label,
  value,
  context,
  currency,
  className = "",
  masked = false,
}: MetricCardProps) {
  const sign = getSign(value);

  return (
    <Card className={className}>
      <h3 className="text-xs font-medium uppercase tracking-wide text-[var(--color-text-tertiary)] mb-2">
        {label}
      </h3>
      <p className={`financial-value text-xl font-semibold tabular-nums ${
        masked
          ? "text-[var(--color-text-primary)]"
          : sign === "+"
            ? "text-positive"
            : sign === "−"
              ? "text-negative"
              : "text-[var(--color-text-primary)]"
      }`}>
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
