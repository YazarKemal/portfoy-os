"use client";

import { useState } from "react";
import { PageHeader } from "@/components/layout/page-header";
import { SectionHeader } from "@/components/ui/section-header";
import { ButtonLink } from "@/components/ui/button";
import { InlineAlert } from "@/components/ui/inline-alert";
import { IconPlus } from "@/components/ui/icons";
import { PortfolioValueHero } from "@/components/dashboard/portfolio-value-hero";
import { MetricCard } from "@/components/dashboard/metric-card";
import { PerformanceChart } from "@/components/dashboard/performance-chart";
import { AllocationBreakdown } from "@/components/dashboard/allocation-breakdown";
import { HoldingsTable } from "@/components/dashboard/holdings-table";
import { HoldingCard } from "@/components/dashboard/holding-card";
import { RecentTransactions } from "@/components/dashboard/recent-transactions";
import { PortfolioObservations } from "@/components/dashboard/portfolio-observations";
import {
  DEMO_METRICS,
  DEMO_PERFORMANCE,
  DEMO_ALLOCATION,
  DEMO_HOLDINGS,
  DEMO_TRANSACTIONS,
  DEMO_OBSERVATIONS,
  DEMO_DATA_FRESHNESS_SUMMARY,
  DEMO_PERIOD_RETURNS,
  PERIOD_CUTOFFS,
  filterPerformanceByPeriod,
} from "@/data/dashboard";
import type { PeriodKey, PrivacyMode } from "@/types/dashboard";

export function DashboardContent() {
  const [period, setPeriod] = useState<PeriodKey>("ALL");
  const [privacy, setPrivacy] = useState<PrivacyMode>("visible");

  const periodReturn = DEMO_PERIOD_RETURNS[period];
  const chartData = filterPerformanceByPeriod(DEMO_PERFORMANCE, PERIOD_CUTOFFS[period]);

  return (
    <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto space-y-8">
      {/* Page Header */}
      <PageHeader
        eyebrow="Konsolide portföy"
        title="Genel Bakış"
        supporting="5 Ağu 2026 · Veriler kısmen güncel"
      >
        <div className="flex items-center gap-3 flex-wrap">
          {/* Portfolio selector */}
          <div className="flex items-center gap-2">
            <label htmlFor="portfolio-select" className="text-xs font-medium text-[var(--color-text-tertiary)] sr-only md:not-sr-only">
              Portföy
            </label>
            <select
              id="portfolio-select"
              className="rounded-[var(--radius-md)] border border-[var(--color-border-strong)] bg-[var(--color-bg-surface)] px-3 py-2 text-sm font-medium text-[var(--color-text-primary)] focus:outline-2 focus:outline-[var(--color-focus)] focus:outline-offset-2 min-h-[44px] min-w-[44px]"
              defaultValue="consolidated"
              aria-label="Portföy seçimi"
            >
              <option value="consolidated">Konsolide portföy</option>
            </select>
          </div>
          <ButtonLink href="/transactions?intent=create" variant="primary">
            <IconPlus size={18} />
            İşlem ekle
          </ButtonLink>
        </div>
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
        totalReturn={periodReturn.amount}
        totalReturnPercent={periodReturn.percentage}
        lastUpdated="5 Ağu 2026, 18:45"
        period={period}
        onPeriodChange={setPeriod}
        privacy={privacy}
        onPrivacyToggle={() =>
          setPrivacy(privacy === "masked" ? "visible" : "masked")
        }
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
            masked={privacy === "masked"}
          />
          <MetricCard
            label="Gerçekleşmemiş kâr/zarar"
            value={DEMO_METRICS.unrealizedPnL}
            context="Açık pozisyonların güncel piyasa değerine göre sonucu"
            masked={privacy === "masked"}
          />
          <MetricCard
            label="Gerçekleşmiş kâr/zarar"
            value={DEMO_METRICS.realizedPnL}
            context="Satışla kesinleşmiş toplam sonuç"
            masked={privacy === "masked"}
          />
          <MetricCard
            label="Nakit ve kısa vadeli rezerv"
            value={DEMO_METRICS.cashReserve}
            context="Hemen kullanılabilir nakit ve nakit benzeri varlıklar"
            masked={privacy === "masked"}
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
            <PerformanceChart
              data={chartData}
              period={period}
              onPeriodChange={setPeriod}
              privacy={privacy}
            />
          </div>
          <div className="lg:col-span-4">
            <AllocationBreakdown items={DEMO_ALLOCATION} masked={privacy === "masked"} />
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
            <HoldingsTable holdings={DEMO_HOLDINGS} masked={privacy === "masked"} />
          </div>
        </div>
        {/* Mobile cards */}
        <div className="flex flex-col gap-4 md:hidden">
          {DEMO_HOLDINGS.map((h) => (
            <HoldingCard key={h.id} holding={h} masked={privacy === "masked"} />
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
            <RecentTransactions transactions={DEMO_TRANSACTIONS} masked={privacy === "masked"} />
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
  );
}
