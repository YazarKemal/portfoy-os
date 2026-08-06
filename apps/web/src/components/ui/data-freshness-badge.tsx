import { IconClock } from "@/components/ui/icons";
import { Badge } from "@/components/ui/badge";
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

  return (
    <Badge variant={variant} className="gap-1">
      <IconClock size={12} aria-hidden="true" />
      {label}
    </Badge>
  );
}
