import type { ReactNode } from "react";
import { IconAlertTriangle, IconCheck, IconInfo } from "./icons";

type AlertKind = "info" | "warning" | "error" | "success";

interface InlineAlertProps {
  kind?: AlertKind;
  children: ReactNode;
  className?: string;
}

const icons: Record<AlertKind, typeof IconAlertTriangle> = {
  info: IconInfo,
  warning: IconAlertTriangle,
  error: IconAlertTriangle,
  success: IconCheck,
};

const styles: Record<AlertKind, string> = {
  info: "bg-[var(--color-info-soft)] text-[var(--color-info)]",
  warning: "bg-[var(--color-warning-soft)] text-[var(--color-warning)]",
  error: "bg-[var(--color-negative-soft)] text-[var(--color-negative)]",
  success: "bg-[var(--color-positive-soft)] text-[var(--color-positive)]",
};

export function InlineAlert({
  kind = "info",
  children,
  className = "",
}: InlineAlertProps) {
  const Icon = icons[kind];
  return (
    <div
      role="alert"
      className={`flex items-start gap-3 rounded-[var(--radius-md)] p-4 text-sm ${styles[kind]} ${className}`}
    >
      <Icon size={18} className="mt-0.5 shrink-0" aria-hidden="true" />
      <div>{children}</div>
    </div>
  );
}
