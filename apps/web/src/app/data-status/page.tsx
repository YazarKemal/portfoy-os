import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { IconDatabase, IconCheck, IconAlertTriangle } from "@/components/ui/icons";
import { DEMO_DATA_SOURCES, DEMO_DATA_FRESHNESS_SUMMARY } from "@/data/dashboard";
import { InlineAlert } from "@/components/ui/inline-alert";

const statusConfig = {
  healthy: { label: "Sağlıklı", variant: "positive" as const, Icon: IconCheck },
  degraded: { label: "Yavaş", variant: "warning" as const, Icon: IconAlertTriangle },
  down: { label: "Kapalı", variant: "negative" as const, Icon: IconAlertTriangle },
  unknown: { label: "Bilinmiyor", variant: "neutral" as const, Icon: IconAlertTriangle },
};

export default function DataStatusPage() {
  return (
    <AppShell>
      <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto space-y-6">
        <PageHeader
          eyebrow="Veri Durumu"
          title="Veri Durumu"
          supporting={DEMO_DATA_FRESHNESS_SUMMARY.label}
        />

        <InlineAlert kind="warning">
          {DEMO_DATA_FRESHNESS_SUMMARY.description}
        </InlineAlert>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {DEMO_DATA_SOURCES.map((src) => {
            const cfg = statusConfig[src.status];
            const StatusIcon = cfg.Icon;
            return (
              <Card key={src.provider}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="flex h-10 w-10 items-center justify-center rounded-[var(--radius-md)] bg-[var(--color-bg-subtle)]">
                      <IconDatabase size={20} className="text-[var(--color-text-secondary)]" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-[var(--color-text-primary)]">
                        {src.providerLabel}
                      </h3>
                      <p className="text-xs text-[var(--color-text-tertiary)]">
                        {src.provider}
                      </p>
                    </div>
                  </div>
                  <Badge variant={cfg.variant}>
                    <StatusIcon size={12} aria-hidden="true" />
                    <span className="ml-1">{cfg.label}</span>
                  </Badge>
                </div>
                <div className="space-y-1 text-xs text-[var(--color-text-tertiary)]">
                  <p>Son kontrol: {src.lastChecked}</p>
                  {src.responseTimeMs !== undefined && src.responseTimeMs > 0 && (
                    <p>Yanıt süresi: {src.responseTimeMs} ms</p>
                  )}
                  {src.lastError && (
                    <p className="text-[var(--color-negative)]">{src.lastError}</p>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </AppShell>
  );
}
