import type { ReactNode } from "react";

type CardVariant = "default" | "subtle" | "inverse" | "interactive";

interface CardProps {
  variant?: CardVariant;
  className?: string;
  children: ReactNode;
  onClick?: () => void;
}

const variantStyles: Record<CardVariant, string> = {
  default:
    "bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)]",
  subtle:
    "bg-[var(--color-bg-subtle)] border border-[var(--color-border-subtle)]",
  inverse:
    "bg-[var(--color-bg-inverse)] text-[var(--color-text-inverse)] border-0",
  interactive:
    "bg-[var(--color-bg-surface)] border border-[var(--color-border-subtle)] hover:border-[var(--color-border-strong)] cursor-pointer transition-colors duration-[var(--motion-standard)]",
};

export function Card({
  variant = "default",
  className = "",
  children,
  onClick,
}: CardProps) {
  const Component = onClick ? "button" : "div";

  const interactiveStyles =
    onClick
      ? "hover:border-[var(--color-border-strong)] cursor-pointer transition-colors duration-[var(--motion-standard)]"
      : "";

  return (
    <Component
      type={onClick ? "button" : undefined}
      className={`rounded-[var(--radius-lg)] p-6 ${interactiveStyles} ${variant === "inverse" ? variantStyles.inverse : variant === "subtle" ? variantStyles.subtle : variantStyles.default} ${className}`}
      onClick={onClick}
    >
      {children}
    </Component>
  );
}
