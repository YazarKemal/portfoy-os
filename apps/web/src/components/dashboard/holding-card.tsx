import Link from "next/link";
import { Card } from "@/components/ui/card";
import { DataFreshnessBadge } from "@/components/ui/data-freshness-badge";
import { IconChevronRight } from "@/components/ui/icons";
import { formatMoney, formatQuantity, formatChange, changeColorClass } from "@/lib/formatters";
import type { Holding } from "@/types/dashboard";

interface HoldingCardProps {
  holding: Holding;
  masked?: boolean;
}

export function HoldingCard({ holding, masked = false }: HoldingCardProps) {
  const daily = formatChange(holding.dailyChange, holding.dailyChangePercent);
  const dailyClass = masked ? "" : changeColorClass(holding.dailyChange);
  const totalSign = masked ? "" : holding.totalPnL > 0 ? "+" : holding.totalPnL < 0 ? "−" : "";
  const totalClass = masked ? "" : changeColorClass(holding.totalPnL);

  return (
    <Card className="space-y-3">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-[var(--color-text-primary)] text-[16px] leading-[24px]">
            {holding.assetName}
          </h3>
          <p className="text-xs text-[var(--color-text-tertiary)]">
            {holding.assetCode} · {holding.assetTypeLabel}
          </p>
        </div>
        <DataFreshnessBadge freshness={holding.dataFreshness} />
      </div>

      <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
        <div>
          <p className="text-xs text-[var(--color-text-tertiary)]">Piyasa Değeri</p>
          <p className="font-semibold tabular-nums text-[var(--color-text-primary)]">
            {masked ? "₺••••••" : formatMoney(holding.marketValue)}
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-text-tertiary)]">Miktar</p>
          <p className="tabular-nums text-[var(--color-text-primary)]">
            {formatQuantity(holding.quantity)}
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-text-tertiary)]">Ort. Maliyet</p>
          <p className="tabular-nums text-[var(--color-text-primary)]">
            {masked ? "₺••••••" : formatMoney(holding.averageCost)}
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-text-tertiary)]">Toplam K/Z</p>
          <p className={`font-medium tabular-nums ${totalClass}`}>
            {masked ? "•••••" : `${totalSign}${formatMoney(Math.abs(holding.totalPnL))}`}
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-[var(--color-border-subtle)] pt-2">
        <p className={`text-xs tabular-nums ${dailyClass}`}>
          Günlük: {masked ? "•••••" : `${daily.amount} (${daily.percentStr})`}
        </p>
        <Link
          href={`/portfolio/${holding.id}`}
          className="inline-flex items-center gap-1 text-xs font-medium text-[var(--color-brand-primary)] hover:underline"
          aria-label={`${holding.assetName} detayını aç`}
        >
          Detay
          <IconChevronRight size={14} aria-hidden="true" />
        </Link>
      </div>
    </Card>
  );
}
