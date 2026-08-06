import Link from "next/link";
import { formatMoney, formatQuantity, formatChange, changeColorClass } from "@/lib/formatters";
import { DataFreshnessBadge } from "@/components/ui/data-freshness-badge";
import { EmptyState } from "@/components/ui/empty-state";
import { IconChevronRight } from "@/components/ui/icons";
import type { Holding } from "@/types/dashboard";

interface HoldingsTableProps {
  holdings: Holding[];
  masked?: boolean;
}

export function HoldingsTable({ holdings, masked = false }: HoldingsTableProps) {
  if (holdings.length === 0) {
    return (
      <EmptyState
        title="Henüz varlık bulunmuyor"
        description="Portföyünüze varlık eklediğinizde burada listelenecektir."
      />
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
            <th scope="col" className="pb-3 pr-4 font-medium text-right">Veri</th>
            <th scope="col" className="pb-3 font-medium text-right">Detay</th>
          </tr>
        </thead>
        <tbody>
          {holdings.map((h) => {
            const daily = formatChange(h.dailyChange, h.dailyChangePercent);
            const totalClass = masked ? "" : changeColorClass(h.totalPnL);
            const dailyClass = masked ? "" : changeColorClass(h.dailyChange);
            const totalSign = masked ? "" : h.totalPnL > 0 ? "+" : h.totalPnL < 0 ? "−" : "";

            return (
              <tr
                key={h.id}
                className="border-b border-[var(--color-border-subtle)]"
              >
                <td className="py-3 pr-4">
                  <span className="font-medium text-[var(--color-text-primary)]">
                    {h.assetName}
                  </span>
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
                  {masked ? "₺••••••" : formatMoney(h.averageCost)}
                </td>
                <td className="py-3 pr-4 text-right tabular-nums text-[var(--color-text-primary)]">
                  {masked ? "₺••••••" : formatMoney(h.currentPrice)}
                </td>
                <td className="py-3 pr-4 text-right tabular-nums font-semibold text-[var(--color-text-primary)]">
                  {masked ? "₺••••••" : formatMoney(h.marketValue)}
                </td>
                <td className={`py-3 pr-4 text-right tabular-nums ${dailyClass}`}>
                  {masked ? "•••••" : `${daily.amount} (${daily.percentStr})`}
                </td>
                <td className={`py-3 pr-4 text-right tabular-nums font-medium ${totalClass}`}>
                  {masked ? "•••••" : `${totalSign}${formatMoney(Math.abs(h.totalPnL))}`}
                </td>
                <td className="py-3 pr-4 text-right">
                  <DataFreshnessBadge freshness={h.dataFreshness} />
                </td>
                <td className="py-3 text-right">
                  <Link
                    href={`/portfolio/${h.id}`}
                    className="inline-flex items-center gap-1 text-xs font-medium text-[var(--color-brand-primary)] hover:underline"
                    aria-label={`${h.assetName} detayını aç`}
                  >
                    Detay
                    <IconChevronRight size={14} aria-hidden="true" />
                  </Link>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
