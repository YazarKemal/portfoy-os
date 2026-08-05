"use client";

import { useState } from "react";
import { Card } from "@/components/ui/card";
import { IconButton } from "@/components/ui/button";
import { IconEye } from "@/components/ui/icons";
import { formatMoney, formatChange } from "@/lib/formatters";
import type { PeriodKey, PrivacyMode } from "@/types/dashboard";

interface PortfolioValueHeroProps {
  totalValue: number;
  dailyChange: number;
  dailyChangePercent: number;
  totalReturn: number;
  totalReturnPercent: number;
  lastUpdated: string;
}

const PERIODS: { key: PeriodKey; label: string }[] = [
  { key: "1A", label: "1A" },
  { key: "3A", label: "3A" },
  { key: "6A", label: "6A" },
  { key: "YBB", label: "YBB" },
  { key: "1Y", label: "1Y" },
  { key: "ALL", label: "Tümü" },
];

export function PortfolioValueHero({
  totalValue,
  dailyChange,
  dailyChangePercent,
  totalReturn,
  totalReturnPercent,
  lastUpdated,
}: PortfolioValueHeroProps) {
  const [period, setPeriod] = useState<PeriodKey>("ALL");
  const [privacy, setPrivacy] = useState<PrivacyMode>("visible");

  const masked = privacy === "masked";
  const daily = formatChange(dailyChange, dailyChangePercent);
  const total = formatChange(totalReturn, totalReturnPercent);

  return (
    <Card variant="inverse" className="relative overflow-hidden">
      {/* Period controls */}
      <div className="flex items-center gap-1 mb-6">
        {PERIODS.map((p) => (
          <button
            key={p.key}
            onClick={() => setPeriod(p.key)}
            className={`rounded-[var(--radius-sm)] px-3 py-1.5 text-xs font-semibold transition-colors duration-[var(--motion-standard)] ${
              period === p.key
                ? "bg-white/20 text-[var(--color-text-inverse)]"
                : "text-[var(--color-text-inverse)]/60 hover:text-[var(--color-text-inverse)] hover:bg-white/10"
            }`}
          >
            {p.label}
          </button>
        ))}
        <div className="ml-auto flex items-center gap-2">
          <IconButton
            label={masked ? "Değerleri göster" : "Değerleri gizle"}
            onClick={() =>
              setPrivacy(masked ? "visible" : "masked")
            }
            className="text-[var(--color-text-inverse)]/60 hover:text-[var(--color-text-inverse)] hover:bg-white/10"
          >
            <IconEye size={18} />
          </IconButton>
        </div>
      </div>

      {/* Value */}
      <div className="mb-2">
        <p className="text-xs font-medium uppercase tracking-wide text-[var(--color-text-inverse)]/60 mb-1">
          Toplam portföy değeri
        </p>
        <p className="financial-display text-[var(--color-text-inverse)] text-[40px] leading-[48px] lg:text-[40px] lg:leading-[48px]">
          {masked
            ? "₺••••••••"
            : formatMoney(totalValue)}
        </p>
      </div>

      {/* Changes */}
      <div className="flex flex-wrap items-center gap-6 mt-4">
        <div>
          <p className="text-xs text-[var(--color-text-inverse)]/50 mb-0.5">Günlük değişim</p>
          <p className={`financial-value text-sm font-semibold tabular-nums ${
            masked
              ? "text-[var(--color-text-inverse)]"
              : dailyChange >= 0
                ? "text-[var(--color-positive-soft)]"
                : "text-[var(--color-negative-soft)]"
          }`}>
            {masked ? "•••••" : `${daily.amount} (${daily.percentStr})`}
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-text-inverse)]/50 mb-0.5">Toplam getiri ({period})</p>
          <p className={`financial-value text-sm font-semibold tabular-nums ${
            masked
              ? "text-[var(--color-text-inverse)]"
              : totalReturn >= 0
                ? "text-[var(--color-positive-soft)]"
                : "text-[var(--color-negative-soft)]"
          }`}>
            {masked ? "•••••" : `${total.amount} (${total.percentStr})`}
          </p>
        </div>
      </div>

      {/* Timestamp */}
      <p className="mt-5 text-xs text-[var(--color-text-inverse)]/40">
        Son hesaplama: {lastUpdated}
      </p>
    </Card>
  );
}
