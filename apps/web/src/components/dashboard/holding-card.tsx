import Link from "next/link";
import { Card } from "@/components/ui/card";
import { DataFreshnessBadge } from "./data-freshness-badge";
import { formatMoney, formatQuantity, formatChange, changeColorClass } from "@/lib/formatters";
import type { Holding } from "@/types/dashboard";

interface HoldingCardProps {
  holding: Holding;
}

export function HoldingCard({ holding }: HoldingCardProps) {
  const daily = formatChange(holding.dailyChange, holding.dailyChangePercent);
  const dailyClass = changeColorClass(holding.dailyChange);
  const totalSign = holding.totalPnL > 0 ? "+" : holding.totalPnL < 0 ? "−" : "";
  const totalClass = changeColorClass(holding.totalPnL);

  return (
    <Card variant="interactive" className="space-y-3">
      <div className="flex items-start justify-between">
        <div>
          <Link
            href={`/portfolio/${holding.id}`}
            className="font-semibold text-[var(--color-brand-primary)] hover:underline text-[16px] leading-[24px]"
          >
            {holding.assetName}
          </Link>
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
            {formatMoney(holding.marketValue)}
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
            {formatMoney(holding.averageCost)}
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-text-tertiary)]">Toplam K/Z</p>
          <p className={`font-medium tabular-nums ${totalClass}`}>
            {totalSign}{formatMoney(Math.abs(holding.totalPnL))}
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-[var(--color-border-subtle)] pt-2">
        <p className={`text-xs tabular-nums ${dailyClass}`}>
          Günlük: {daily.amount} ({daily.percentStr})
        </p>
        <Link
          href={`/portfolio/${holding.id}`}
          className="text-xs font-medium text-[var(--color-brand-primary)] hover:underline"
        >
          Detay →
        </Link>
      </div>
    </Card>
  );
}
