import { AppShell } from "@/components/layout/app-shell";
import { Skeleton } from "@/components/ui/skeleton";
import { SectionHeader } from "@/components/ui/section-header";

export default function Loading() {
  return (
    <AppShell>
      <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto space-y-8">
        {/* Page header skeleton */}
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div className="space-y-2">
            <Skeleton className="h-3 w-28" />
            <Skeleton className="h-9 w-44" />
            <Skeleton className="h-4 w-48" />
          </div>
          <Skeleton className="h-11 w-36" />
        </div>

        {/* Hero skeleton */}
        <Skeleton className="h-56 w-full rounded-[var(--radius-lg)]" />

        {/* Metric cards skeleton */}
        <section aria-labelledby="metrics-heading-loading">
          <SectionHeader title="Öne Çıkan Metrikler" id="metrics-heading-loading" className="mb-4" />
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} className="h-28 rounded-[var(--radius-lg)]" />
            ))}
          </div>
        </section>

        {/* Chart + Allocation skeleton */}
        <section aria-labelledby="perf-heading-loading">
          <SectionHeader title="Performans ve Dağılım" id="perf-heading-loading" className="mb-4" />
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <Skeleton className="lg:col-span-8 h-[300px] rounded-[var(--radius-lg)]" />
            <Skeleton className="lg:col-span-4 h-[300px] rounded-[var(--radius-lg)]" />
          </div>
        </section>

        {/* Holdings skeleton */}
        <section aria-labelledby="holdings-heading-loading">
          <SectionHeader title="Varlıklar" id="holdings-heading-loading" className="mb-4" />
          <Skeleton className="h-64 rounded-[var(--radius-lg)]" />
        </section>

        {/* Bottom skeleton */}
        <section aria-labelledby="activity-heading-loading">
          <SectionHeader title="Son İşlemler ve Gözlemler" id="activity-heading-loading" className="mb-4" />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Skeleton className="lg:col-span-2 h-64 rounded-[var(--radius-lg)]" />
            <Skeleton className="lg:col-span-1 h-64 rounded-[var(--radius-lg)]" />
          </div>
        </section>
      </div>
    </AppShell>
  );
}
