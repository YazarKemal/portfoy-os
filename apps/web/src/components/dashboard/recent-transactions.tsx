import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { IconPlus } from "@/components/ui/icons";
import { formatMoney, formatQuantity } from "@/lib/formatters";
import type { TransactionItem } from "@/types/dashboard";

interface RecentTransactionsProps {
  transactions: TransactionItem[];
}

const typeIcons: Record<string, string> = {
  BUY: "→",
  SELL: "←",
  DEPOSIT: "↓",
  WITHDRAWAL: "↑",
  DIVIDEND: "✦",
  INTEREST: "✦",
  FEE: "✕",
  TAX: "✕",
  TRANSFER_IN: "↓",
  TRANSFER_OUT: "↑",
};

export function RecentTransactions({ transactions }: RecentTransactionsProps) {
  if (transactions.length === 0) {
    return (
      <Card>
        <p className="text-sm text-[var(--color-text-tertiary)] text-center py-8">
          Henüz işlem kaydı bulunmuyor.
        </p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-[16px] leading-[24px] font-semibold text-[var(--color-text-primary)]">
          Son İşlemler
        </h3>
        <Link
          href="/transactions"
          className="text-xs font-medium text-[var(--color-brand-primary)] hover:underline"
        >
          Tüm işlemleri gör
        </Link>
      </div>

      <ul className="divide-y divide-[var(--color-border-subtle)]">
        {transactions.map((tx) => (
          <li key={tx.id} className="flex items-center gap-3 py-3 first:pt-0 last:pb-0">
            {/* Type icon */}
            <span
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-bg-subtle)] text-sm font-semibold text-[var(--color-text-secondary)]"
              aria-hidden="true"
            >
              {typeIcons[tx.type] ?? "·"}
            </span>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-[var(--color-text-primary)] truncate">
                  {tx.typeLabel}
                </span>
                {tx.needsReview && (
                  <Badge variant="warning">İncelenmeli</Badge>
                )}
              </div>
              <p className="text-xs text-[var(--color-text-tertiary)]">
                {tx.assetName} · {tx.accountName}
              </p>
            </div>

            <div className="text-right shrink-0">
              <p className="text-sm font-semibold tabular-nums text-[var(--color-text-primary)]">
                {formatMoney(tx.totalValue)}
              </p>
              <p className="text-xs text-[var(--color-text-tertiary)]">
                {tx.quantity ? `${formatQuantity(tx.quantity)} adet · ` : ""}{tx.date}
              </p>
            </div>
          </li>
        ))}
      </ul>

      <div className="mt-4 border-t border-[var(--color-border-subtle)] pt-4">
        <Button variant="primary" className="w-full">
          <IconPlus size={18} />
          İşlem ekle
        </Button>
      </div>
    </Card>
  );
}
