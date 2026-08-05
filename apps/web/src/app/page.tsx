import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { SectionHeader } from "@/components/ui/section-header";
import { Button } from "@/components/ui/button";
import { IconPlus } from "@/components/ui/icons";
import { PortfolioValueHero } from "@/components/dashboard/portfolio-value-hero";
import { MetricCard } from "@/components/dashboard/metric-card";
import { PerformanceChart } from "@/components/dashboard/performance-chart";
import { AllocationBreakdown } from "@/components/dashboard/allocation-breakdown";
import { HoldingsTable } from "@/components/dashboard/holdings-table";
import { HoldingCard } from "@/components/dashboard/holding-card";
import { RecentTransactions } from "@/components/dashboard/recent-transactions";
import { PortfolioObservations } from "@/components/dashboard/portfolio-observations";
import { InlineAlert } from "@/components/ui/inline-alert";
import {
  DEMO_METRICS,
  DEMO_PERFORMANCE,
  DEMO_ALLOCATION,
  DEMO_HOLDINGS,
  DEMO_TRANSACTIONS,
  DEMO_OBSERVATIONS,
  DEMO_DATA_FRESHNESS_SUMMARY,
} from "@/data/dashboard";

export default function DashboardPage() {
  return (
    <AppShell>
      <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto space-y-8">
        {/* Page Header */}
        <PageHeader
          eyebrow="Konsolide portföy"
          title="Genel Bakış"
          supporting="5 Ağu 2026 · Veriler kısmen güncel"
        >
          <Button>
            <IconPlus size={18} />
            İşlem ekle
          </Button>
        </PageHeader>

        {/* Stale data alert */}
        <InlineAlert kind="warning">
          {DEMO_DATA_FRESHNESS_SUMMARY.description}
        </InlineAlert>

        {/* Hero */}
        <PortfolioValueHero
          totalValue={DEMO_METRICS.totalValue}
          dailyChange={DEMO_METRICS.dailyChange}
          dailyChangePercent={DEMO_METRICS.dailyChangePercent}
          totalReturn={DEMO_METRICS.totalReturn}
          totalReturnPercent={DEMO_METRICS.totalReturnPercent}
          lastUpdated="5 Ağu 2026, 18:45"
        />

        {/* Key Metrics */}
        <section aria-labelledby="metrics-heading">
          <SectionHeader
            title="Öne Çıkan Metrikler"
            id="metrics-heading"
            className="mb-4"
          />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              label="Yatırılan ana para"
              value={DEMO_METRICS.investedPrincipal}
              context="Portföye yatırılan toplam anapara tutarı"
            />
            <MetricCard
              label="Gerçekleşmemiş kâr/zarar"
              value={DEMO_METRICS.unrealizedPnL}
              context="Açık pozisyonların güncel piyasa değerine göre sonucu"
            />
            <MetricCard
              label="Gerçekleşmiş kâr/zarar"
              value={DEMO_METRICS.realizedPnL}
              context="Satışla kesinleşmiş toplam sonuç"
            />
            <MetricCard
              label="Nakit ve kısa vadeli rezerv"
              value={DEMO_METRICS.cashReserve}
              context="Hemen kullanılabilir nakit ve nakit benzeri varlıklar"
            />
          </div>
        </section>

        {/* Performance + Allocation */}
        <section aria-labelledby="perf-heading">
          <SectionHeader
            title="Performans ve Dağılım"
            id="perf-heading"
            className="mb-4"
          />
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-8">
              <PerformanceChart data={DEMO_PERFORMANCE} />
            </div>
            <div className="lg:col-span-4">
              <AllocationBreakdown items={DEMO_ALLOCATION} />
            </div>
          </div>
        </section>

        {/* Holdings */}
        <section aria-labelledby="holdings-heading">
          <SectionHeader
            title="Varlıklar"
            id="holdings-heading"
            className="mb-4"
          />
          {/* Desktop/Tablet table */}
          <div className="hidden md:block">
            <div className="bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] rounded-[var(--radius-lg)] p-6">
              <HoldingsTable holdings={DEMO_HOLDINGS} />
            </div>
          </div>
          {/* Mobile cards */}
          <div className="flex flex-col gap-4 md:hidden">
            {DEMO_HOLDINGS.map((h) => (
              <HoldingCard key={h.id} holding={h} />
            ))}
          </div>
        </section>

        {/* Recent Transactions + Observations */}
        <section aria-labelledby="activity-heading">
          <SectionHeader
            title="Son İşlemler ve Gözlemler"
            id="activity-heading"
            className="mb-4"
          />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <RecentTransactions transactions={DEMO_TRANSACTIONS} />
            </div>
            <div className="lg:col-span-1">
              <PortfolioObservations observations={DEMO_OBSERVATIONS} />
            </div>
          </div>
        </section>

        {/* Demo data notice */}
        <p className="text-center text-[10px] text-[var(--color-text-tertiary)] py-4">
          Demo veri · Bu gösterge paneli kurgusal portföy değerleri içerir, yatırım tavsiyesi niteliği taşımaz.
        </p>
      </div>
    </AppShell>
  );
}
