import { IconClock } from "@/components/ui/icons";
import type { DataFreshness } from "@/types/dashboard";

interface DataFreshnessBadgeProps {
  freshness: DataFreshness;
}

const config: Record<DataFreshness, { label: string; variant: "positive" | "warning" | "negative" | "neutral" }> = {
  live: { label: "Canlı", variant: "positive" },
  delayed: { label: "Gecikmeli", variant: "warning" },
  eod: { label: "Gün sonu", variant: "neutral" },
  stale: { label: "Eski", variant: "negative" },
};

export function DataFreshnessBadge({ freshness }: DataFreshnessBadgeProps) {
  const { label, variant } = config[freshness];

  const variantColors: Record<string, string> = {
    positive: "bg-[var(--color-positive-soft)] text-[var(--color-positive)]",
    warning: "bg-[var(--color-warning-soft)] text-[var(--color-warning)]",
    negative: "bg-[var(--color-negative-soft)] text-[var(--color-negative)]",
    neutral: "bg-[var(--color-bg-subtle)] text-[var(--color-text-tertiary)]",
  };

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium ${variantColors[variant]}`}
      title={`Veri durumu: ${label}`}
      aria-label={`Veri durumu: ${label}`}
    >
      <IconClock size={12} aria-hidden="true" />
      {label}
    </span>
  );
}
