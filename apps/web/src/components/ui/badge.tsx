import type { ReactNode } from "react";

type BadgeVariant = "neutral" | "positive" | "negative" | "warning" | "info";

interface BadgeProps {
  variant?: BadgeVariant;
  children: ReactNode;
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  neutral:
    "bg-[var(--color-bg-subtle)] text-[var(--color-text-secondary)] border-[var(--color-border-subtle)]",
  positive:
    "bg-[var(--color-positive-soft)] text-[var(--color-positive)] border-transparent",
  negative:
    "bg-[var(--color-negative-soft)] text-[var(--color-negative)] border-transparent",
  warning:
    "bg-[var(--color-warning-soft)] text-[var(--color-warning)] border-transparent",
  info: "bg-[var(--color-info-soft)] text-[var(--color-info)] border-transparent",
};

export function Badge({
  variant = "neutral",
  className = "",
  children,
}: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
