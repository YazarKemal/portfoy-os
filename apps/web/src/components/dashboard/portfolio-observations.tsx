import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { IconAlertTriangle, IconInfo } from "@/components/ui/icons";
import type { PortfolioObservation } from "@/types/dashboard";

interface PortfolioObservationsProps {
  observations: PortfolioObservation[];
}

const kindIcon = {
  concentration: IconAlertTriangle,
  "data-quality": IconAlertTriangle,
  allocation: IconInfo,
  risk: IconAlertTriangle,
};

const kindColor = {
  concentration: "text-[var(--color-warning)]",
  "data-quality": "text-[var(--color-warning)]",
  allocation: "text-[var(--color-info)]",
  risk: "text-[var(--color-warning)]",
};

export function PortfolioObservations({ observations }: PortfolioObservationsProps) {
  if (observations.length === 0) {
    return (
      <EmptyState
        title="Gözlem bulunmuyor"
        description="Portföyünüzle ilgili gözlemler burada listelenecektir."
      />
    );
  }

  return (
    <Card variant="subtle" className="h-full flex flex-col">
      <h3 className="text-[16px] leading-[24px] font-semibold text-[var(--color-text-primary)] mb-3">
        Portföy gözlemleri
      </h3>
      <ul className="space-y-2.5">
        {observations.map((obs) => {
          const Icon = kindIcon[obs.kind];
          const color = kindColor[obs.kind];
          return (
            <li key={obs.id} className="flex items-start gap-2.5 text-sm">
              <Icon size={16} className={`mt-0.5 shrink-0 ${color}`} aria-hidden="true" />
              <span className="text-[var(--color-text-secondary)]">{obs.text}</span>
            </li>
          );
        })}
      </ul>
      <p className="mt-auto pt-4 text-xs text-[var(--color-text-tertiary)]">
        Bu gözlemler deterministik portföy kurallarına dayanır, yatırım tavsiyesi değildir.
      </p>
    </Card>
  );
}
