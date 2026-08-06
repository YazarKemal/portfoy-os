interface SpinnerProps {
  label?: string;
  size?: number;
  className?: string;
}

export function Spinner({ label = "Yükleniyor", size = 24, className = "" }: SpinnerProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      className={`animate-spin ${className}`}
      role="status"
      aria-label={label}
      style={{ animationDuration: "0.8s" }}
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="var(--color-border-subtle)"
        strokeWidth="3"
      />
      <path
        d="M12 2a10 10 0 019.95 9"
        stroke="var(--color-brand-primary)"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}
