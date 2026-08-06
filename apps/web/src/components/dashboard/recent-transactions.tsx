import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { ButtonLink } from "@/components/ui/button";
import {
  IconArrowDown,
  IconArrowUp,
  IconArrowRight,
  IconArrowLeft,
  IconPercent,
  IconMinus,
  IconPlus,
} from "@/components/ui/icons";
import { formatMoney, formatQuantity } from "@/lib/formatters";
import type { ReactNode } from "react";
import type { TransactionItem, TransactionTypeLabel } from "@/types/dashboard";

interface RecentTransactionsProps {
  transactions: TransactionItem[];
  masked?: boolean;
}

const typeIcons: Record<TransactionTypeLabel, ReactNode> = {
  BUY: <IconArrowRight size={16} aria-hidden="true" />,
  SELL: <IconArrowLeft size={16} aria-hidden="true" />,
  DEPOSIT: <IconArrowDown size={16} aria-hidden="true" />,
  WITHDRAWAL: <IconArrowUp size={16} aria-hidden="true" />,
  DIVIDEND: <IconPercent size={16} aria-hidden="true" />,
  INTEREST: <IconPercent size={16} aria-hidden="true" />,
  FEE: <IconMinus size={16} aria-hidden="true" />,
  TAX: <IconMinus size={16} aria-hidden="true" />,
  TRANSFER_IN: <IconArrowDown size={16} aria-hidden="true" />,
  TRANSFER_OUT: <IconArrowUp size={16} aria-hidden="true" />,
};

export function RecentTransactions({ transactions, masked = false }: RecentTransactionsProps) {
  if (transactions.length === 0) {
    return (
      <EmptyState
        title="Henüz işlem kaydı bulunmuyor"
        description="İlk işleminizi ekleyerek portföyünüzü takip etmeye başlayabilirsiniz."
      />
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
              className="flex h-9 w-9 shrink-0 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-bg-subtle)] text-[var(--color-text-secondary)]"
              aria-hidden="true"
            >
              {typeIcons[tx.type] ?? <IconMinus size={16} aria-hidden="true" />}
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
                {masked ? "₺••••••" : formatMoney(tx.totalValue)}
              </p>
              <p className="text-xs text-[var(--color-text-tertiary)]">
                {tx.quantity ? `${formatQuantity(tx.quantity)} adet · ` : ""}{tx.date}
              </p>
            </div>
          </li>
        ))}
      </ul>

      <div className="mt-4 border-t border-[var(--color-border-subtle)] pt-4">
        <ButtonLink href="/transactions?intent=create" variant="primary" className="w-full">
          <IconPlus size={18} />
          İşlem ekle
        </ButtonLink>
      </div>
    </Card>
  );
}
