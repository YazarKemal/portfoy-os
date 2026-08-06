import type { ReactNode } from "react";
import { IconFileText } from "./icons";

interface EmptyStateProps {
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({
  title,
  description,
  action,
  className = "",
}: EmptyStateProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center rounded-[var(--radius-lg)] border border-dashed border-[var(--color-border-strong)] bg-[var(--color-bg-surface)] px-8 py-16 text-center ${className}`}
    >
      <IconFileText size={40} className="text-[var(--color-text-tertiary)] mb-4" strokeWidth={1.2} />
      <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
        {title}
      </h3>
      {description && (
        <p className="mt-2 max-w-md text-sm text-[var(--color-text-tertiary)]">
          {description}
        </p>
      )}
      {action && <div className="mt-6">{action}</div>}
    </div>
  );
}
