import Link from "next/link";
import { formatMoney, formatQuantity, formatChange, changeColorClass } from "@/lib/formatters";
import { DataFreshnessBadge } from "./data-freshness-badge";
import type { Holding } from "@/types/dashboard";

interface HoldingsTableProps {
  holdings: Holding[];
}

export function HoldingsTable({ holdings }: HoldingsTableProps) {
  if (holdings.length === 0) {
    return (
      <p className="text-sm text-[var(--color-text-tertiary)] text-center py-16">
        Henüz varlık bulunmuyor.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto custom-scrollbar">
      <table className="w-full text-sm" aria-label="Varlıklar">
        <caption className="sr-only">
          Portföydeki varlıkların detaylı listesi. Sütunlar: Varlık, Tür, Miktar, Ortalama Maliyet, Güncel Fiyat, Piyasa Değeri, Günlük Değişim, Toplam Kâr/Zarar, Veri Zamanı.
        </caption>
        <thead>
          <tr className="border-b border-[var(--color-border-subtle)] text-left text-xs font-medium uppercase tracking-wide text-[var(--color-text-tertiary)]">
            <th scope="col" className="pb-3 pr-4 font-medium">Varlık</th>
            <th scope="col" className="pb-3 pr-4 font-medium">Tür</th>
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Miktar</th>
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Ort. Maliyet</th>
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Güncel Fiyat</th>
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Piyasa Değeri</th>
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Günlük Değişim</th>
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Toplam K/Z</th>
            <th scope="col" className="pb-3 font-medium text-right">Veri</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((h) => {
            const daily = formatChange(h.dailyChange, h.dailyChangePercent);
            const totalClass = changeColorClass(h.totalPnL);
            const totalSign = h.totalPnL > 0 ? "+" : h.totalPnL < 0 ? "−" : "";

            return (
              <tr
                key={h.id}
                className="border-b border-[var(--color-border-subtle)] hover:bg-[var(--color-bg-subtle)] transition-colors duration-[var(--motion-standard)]"
              >
                <td className="py-3 pr-4">
                  <Link
                    href={`/portfolio/${h.id}`}
                    className="font-medium text-[var(--color-brand-primary)] hover:underline"
                  >
                    {h.assetName}
                  </Link>
                  <p className="text-xs text-[var(--color-text-tertiary)]">
                    {h.assetCode}
                  </p>
                </td>
                <td className="py-3 pr-4 text-[var(--color-text-secondary)]">
                  {h.assetTypeLabel}
                </td>
                <td className="py-3 pr-4 text-right tabular-nums text-[var(--color-text-primary)]">
                  {formatQuantity(h.quantity)}
                </td>
                <td className="py-3 pr-4 text-right tabular-nums text-[var(--color-text-primary)]">
                  {formatMoney(h.averageCost)}
                </td>
                <td className="py-3 pr-4 text-right tabular-nums text-[var(--color-text-primary)]">
                  {formatMoney(h.currentPrice)}
                </td>
                <td className="py-3 pr-4 text-right tabular-nums font-semibold text-[var(--color-text-primary)]">
                  {formatMoney(h.marketValue)}
                </td>
                <td className={`py-3 pr-4 text-right tabular-nums ${changeColorClass(h.dailyChange)}`}>
                  {daily.amount} ({daily.percentStr})
                </td>
                <td className={`py-3 pr-4 text-right tabular-nums font-medium ${totalClass}`}>
                  {totalSign}{formatMoney(Math.abs(h.totalPnL))}
                </td>
                <td className="py-3 text-right">
                  <DataFreshnessBadge freshness={h.dataFreshness} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
