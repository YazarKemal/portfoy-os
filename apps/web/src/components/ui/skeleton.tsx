interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className = "" }: SkeletonProps) {
  return (
    <div
      className={`animate-pulse rounded-[var(--radius-md)] bg-[var(--color-bg-subtle)] ${className}`}
      aria-hidden="true"
      role="presentation"
      style={{ animationDuration: "1.5s" }}
    />
  );
}
