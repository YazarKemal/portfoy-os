import type { ReactNode } from "react";

interface PageHeaderProps {
  eyebrow?: string;
  title: string;
  supporting?: string;
  children?: ReactNode;
  className?: string;
}

export function PageHeader({
  eyebrow,
  title,
  supporting,
  children,
  className = "",
}: PageHeaderProps) {
  return (
    <div
      className={`flex flex-wrap items-end justify-between gap-4 ${className}`}
    >
      <div>
        {eyebrow && (
          <p className="text-xs font-medium uppercase tracking-wide text-[var(--color-text-tertiary)] mb-1">
            {eyebrow}
          </p>
        )}
        <h1 className="text-[28px] leading-[36px] font-semibold text-[var(--color-text-primary)]">
          {title}
        </h1>
        {supporting && (
          <p className="mt-1 text-sm text-[var(--color-text-tertiary)]">
            {supporting}
          </p>
        )}
      </div>
      {children && <div className="flex items-center gap-3">{children}</div>}
    </div>
  );
}
