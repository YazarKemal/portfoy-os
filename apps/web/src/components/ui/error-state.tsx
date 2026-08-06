import type { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { IconAlertTriangle, IconRefresh } from "@/components/ui/icons";

interface ErrorStateProps {
  title: string;
  description?: string;
  onRetry?: () => void;
  secondaryAction?: ReactNode;
  className?: string;
}

export function ErrorState({
  title,
  description,
  onRetry,
  secondaryAction,
  className = "",
}: ErrorStateProps) {
  return (
    <div
      role="alert"
      className={`flex flex-col items-center justify-center rounded-[var(--radius-lg)] border border-[var(--color-border-subtle)] bg-[var(--color-bg-surface)] px-8 py-16 text-center ${className}`}
    >
      <IconAlertTriangle
        size={40}
        className="text-[var(--color-warning)] mb-4"
        strokeWidth={1.2}
        aria-hidden="true"
      />
      <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">
        {title}
      </h2>
      {description && (
        <p className="mt-2 max-w-md text-sm text-[var(--color-text-tertiary)]">
          {description}
        </p>
      )}
      <div className="mt-6 flex items-center gap-3">
        {onRetry && (
          <Button variant="secondary" onClick={onRetry}>
            <IconRefresh size={18} />
            Tekrar dene
          </Button>
        )}
        {secondaryAction}
      </div>
    </div>
  );
}
