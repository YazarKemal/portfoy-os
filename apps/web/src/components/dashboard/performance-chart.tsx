"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { formatMoney, formatCompactMoney } from "@/lib/formatters";
import type { PerformancePoint, PeriodKey, PrivacyMode } from "@/types/dashboard";

interface PerformanceChartProps {
  data: PerformancePoint[];
  period: PeriodKey;
  privacy: PrivacyMode;
}

const PERIOD_LABELS: Record<PeriodKey, string> = {
  "1A": "1A",
  "3A": "3A",
  "6A": "6A",
  YBB: "YBB",
  "1Y": "1Y",
  ALL: "Tümü",
};

export function PerformanceChart({ data, period, privacy }: PerformanceChartProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const masked = privacy === "masked";

  if (data.length < 2) {
    return (
      <Card>
        <p className="text-sm text-[var(--color-text-tertiary)] text-center py-16">
          Grafik için yeterli veri bulunmuyor.
        </p>
      </Card>
    );
  }

  const values = data.map((d) => d.value);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const padding = 24;
  const rightGutter = 56;
  const width = 600 + rightGutter;
  const height = 220;
  const chartH = height - padding * 2;

  const toX = (i: number) =>
    padding + (i / (data.length - 1)) * (width - padding * 2 - rightGutter);
  const toY = (v: number) =>
    height - padding - ((v - min) / range) * chartH;

  const linePath = data
    .map((d, i) => `${i === 0 ? "M" : "L"}${toX(i)},${toY(d.value)}`)
    .join(" ");

  const areaPath = `${linePath} L${toX(data.length - 1)},${height - padding} L${toX(0)},${height - padding} Z`;

  const principalLine = data[0].principal
    ? data
        .map(
          (d, i) =>
            `${i === 0 ? "M" : "L"}${toX(i)},${toY(d.principal ?? d.value)}`,
        )
        .join(" ")
    : null;

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-[16px] leading-[24px] font-semibold text-[var(--color-text-primary)]">
          Performans
        </h3>
        <span className="rounded-[var(--radius-sm)] bg-[var(--color-bg-subtle)] px-2.5 py-1 text-xs font-medium text-[var(--color-text-tertiary)]">
          Seçili dönem: {PERIOD_LABELS[period]}
        </span>
      </div>

      <div className="relative" role="img" aria-label={masked ? "Gizlilik modu açık. Grafik değerleri maskelenmiştir." : "Portföy değeri performans grafiği. Portföy değeri zaman içinde artış göstermiştir."}>
        {masked && (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-[var(--color-bg-surface)]/80 rounded-[var(--radius-sm)]">
            <span className="text-sm font-medium text-[var(--color-text-tertiary)]">
              Gizlilik modu açık
            </span>
          </div>
        )}

        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto"
          style={{ maxHeight: height }}
          aria-hidden="true"
        >
          {/* Grid lines */}
          {[min, min + range * 0.25, min + range * 0.5, min + range * 0.75, max].map((v, i) => (
            <g key={i}>
              <line
                x1={padding}
                y1={toY(v)}
                x2={width - padding - rightGutter}
                y2={toY(v)}
                stroke="var(--color-border-subtle)"
                strokeWidth={0.5}
                strokeDasharray="4 4"
              />
              <text
                x={width - padding - rightGutter + 8}
                y={toY(v) + 3}
                className="text-[10px]"
                fill="var(--color-text-tertiary)"
                textAnchor="start"
              >
                {masked ? "••••" : formatCompactMoney(v)}
              </text>
            </g>
          ))}

          {/* Area */}
          <path d={areaPath} fill="var(--color-brand-soft)" opacity={0.5} />

          {/* Principal line */}
          {principalLine && (
            <path
              d={principalLine}
              stroke="var(--color-text-tertiary)"
              strokeWidth={1}
              strokeDasharray="6 4"
              fill="none"
              opacity={0.5}
            />
          )}

          {/* Value line */}
          <path
            d={linePath}
            stroke="var(--color-brand-primary)"
            strokeWidth={2}
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* Dot markers */}
          {data.map((d, i) => (
            <circle
              key={i}
              cx={toX(i)}
              cy={toY(d.value)}
              r={activeIndex === i ? 5 : 2.5}
              fill={
                activeIndex === i
                  ? "var(--color-brand-primary)"
                  : "var(--color-bg-surface)"
              }
              stroke="var(--color-brand-primary)"
              strokeWidth={1.5}
              className="transition-all duration-[var(--motion-standard)] cursor-pointer"
              onMouseEnter={() => setActiveIndex(i)}
              onMouseLeave={() => setActiveIndex(null)}
            />
          ))}
        </svg>

        {/* Tooltip */}
        {activeIndex !== null && !masked && (
          <div
            className="absolute top-2 rounded-[var(--radius-sm)] border border-[var(--color-border-subtle)] bg-[var(--color-bg-surface)] px-3 py-2 text-xs shadow-sm"
            style={{
              left: `${Math.min(Math.max(((activeIndex / (data.length - 1)) * 100), 5), 85)}%`,
            }}
          >
            <p className="text-[var(--color-text-tertiary)]">
              {new Date(data[activeIndex].date).toLocaleDateString("tr-TR", {
                day: "numeric",
                month: "short",
              })}
            </p>
            <p className="font-semibold tabular-nums text-[var(--color-text-primary)]">
              {formatMoney(data[activeIndex].value)}
            </p>
          </div>
        )}

        {/* Screen reader summary */}
        <div className="sr-only">
          {masked
            ? "Gizlilik modu açık. Grafik değerleri maskelenmiştir."
            : `Performans grafiği: Portföy değeri ${formatMoney(data[0].value)} seviyesinden ${formatMoney(data[data.length - 1].value)} seviyesine yükselmiştir.`}
        </div>
      </div>

      {/* Legend */}
      <div className="mt-3 flex items-center gap-6 text-xs text-[var(--color-text-tertiary)]">
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-2.5 w-2.5 rounded-full bg-[var(--color-brand-primary)]" aria-hidden="true" />
          Portföy değeri
        </span>
        {data[0].principal && (
          <span className="flex items-center gap-1.5">
            <span className="inline-block h-px w-4 border-t border-dashed border-[var(--color-text-tertiary)]" aria-hidden="true" />
            Yatırılan ana para
          </span>
        )}
      </div>
    </Card>
  );
}
