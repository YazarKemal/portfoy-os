"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import type { IconProps } from "@/components/ui/icons";
import {
  IconHome,
  IconBriefcase,
  IconArrowsExchange,
  IconChart,
  IconMenu,
} from "@/components/ui/icons";

interface MobileNavItem {
  href: string;
  label: string;
  icon: (props: IconProps) => ReactNode;
  disabled?: boolean;
}

const items: MobileNavItem[] = [
  { href: "/", label: "Genel Bakış", icon: IconHome },
  { href: "/portfolio", label: "Portföy", icon: IconBriefcase },
  { href: "/transactions", label: "İşlemler", icon: IconArrowsExchange },
  { href: "#", label: "Analiz", icon: IconChart, disabled: true },
  { href: "#", label: "Daha Fazla", icon: IconMenu, disabled: true },
];

export function MobileNavigation() {
  const pathname = usePathname();

  return (
    <nav
      className="fixed inset-x-0 bottom-0 z-40 border-t border-[var(--color-border-subtle)] bg-[var(--color-bg-surface)] md:hidden"
      aria-label="Mobil menü"
    >
      <ul className="flex h-16 items-center justify-around px-2">
        {items.map((item) => {
          const isActive = !item.disabled && pathname === item.href;
          const Icon = item.icon;

          const content = (
            <span className="flex flex-col items-center gap-0.5">
              <Icon
                size={20}
                aria-hidden="true"
                className={
                  isActive
                    ? "text-[var(--color-brand-primary)]"
                    : "text-[var(--color-text-tertiary)]"
                }
              />
              <span
                className={`text-[10px] font-medium leading-tight ${
                  isActive
                    ? "text-[var(--color-brand-primary)]"
                    : "text-[var(--color-text-tertiary)]"
                } ${item.disabled ? "opacity-50" : ""}`}
              >
                {item.label}
              </span>
            </span>
          );

          if (item.disabled) {
            return (
              <li key={item.label}>
                <span className="flex items-center justify-center min-h-[44px] min-w-[44px] cursor-not-allowed" aria-disabled="true">
                  {content}
                </span>
              </li>
            );
          }

          return (
            <li key={item.label}>
              <Link
                href={item.href}
                className="flex items-center justify-center min-h-[44px] min-w-[44px]"
                aria-current={isActive ? "page" : undefined}
              >
                {content}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
