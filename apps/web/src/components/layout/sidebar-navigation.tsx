"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  IconHome,
  IconBriefcase,
  IconArrowsExchange,
  IconChart,
  IconStar,
  IconDatabase,
  IconSettings,
} from "@/components/ui/icons";
import { Badge } from "@/components/ui/badge";
import type { ReactNode } from "react";
import type { IconProps } from "@/components/ui/icons";

interface NavItem {
  href: string;
  label: string;
  icon: (props: IconProps) => ReactNode;
  disabled?: boolean;
  badge?: string;
}

const primaryItems: NavItem[] = [
  { href: "/", label: "Genel Bakış", icon: IconHome },
  { href: "/portfolio", label: "Portföyüm", icon: IconBriefcase },
  { href: "/transactions", label: "İşlemler", icon: IconArrowsExchange },
  { href: "#", label: "Analiz", icon: IconChart, disabled: true, badge: "Yakında" },
  { href: "#", label: "İzleme Listesi", icon: IconStar, disabled: true, badge: "Yakında" },
  { href: "/data-status", label: "Veri Durumu", icon: IconDatabase },
];

const secondaryItems: NavItem[] = [
  { href: "/settings", label: "Ayarlar", icon: IconSettings },
];

function SidebarNavItem({ item, collapsed }: { item: NavItem; collapsed: boolean }) {
  const pathname = usePathname();
  const isActive = !item.disabled && pathname === item.href;
  const Icon = item.icon;

  const baseClasses =
    "flex items-center gap-3 rounded-[var(--radius-md)] px-3 py-2.5 text-sm font-medium transition-colors duration-[var(--motion-standard)]";

  const activeClasses = isActive
    ? "bg-[var(--color-brand-soft)] text-[var(--color-brand-primary)]"
    : "text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-subtle)] hover:text-[var(--color-text-primary)]";

  const collapsedClasses = collapsed
    ? "justify-center min-h-[44px] min-w-[44px] p-0"
    : "";

  const content = (
    <>
      <Icon size={20} aria-hidden="true" />
      {!collapsed && <span>{item.label}</span>}
      {!collapsed && item.badge && (
        <Badge variant="neutral" className="ml-auto">
          {item.badge}
        </Badge>
      )}
      {/* Yakında indicator for collapsed disabled items */}
      {collapsed && item.disabled && (
        <span className="sr-only"> — Yakında</span>
      )}
    </>
  );

  if (item.disabled) {
    return (
      <span
        className={`${baseClasses} ${activeClasses} ${collapsedClasses} cursor-not-allowed opacity-60`}
        aria-disabled="true"
        aria-label={collapsed ? `${item.label}, Yakında` : undefined}
        title={item.badge ?? undefined}
      >
        {content}
        {/* Lock/dot indicator for collapsed disabled */}
        {collapsed && (
          <span
            className="absolute bottom-1 right-1 h-1.5 w-1.5 rounded-full bg-[var(--color-text-tertiary)]"
            aria-hidden="true"
          />
        )}
      </span>
    );
  }

  return (
    <Link
      href={item.href}
      className={`${baseClasses} ${activeClasses} ${collapsedClasses}`}
      aria-current={isActive ? "page" : undefined}
    >
      {content}
    </Link>
  );
}

export function SidebarNavigation() {
  return (
    <nav className="flex flex-1 flex-col gap-1 overflow-y-auto px-3 py-4 custom-scrollbar" aria-label="Ana menü">
      {primaryItems.map((item) => (
        <SidebarNavItem key={item.label} item={item} collapsed={false} />
      ))}
      <div className="mt-auto border-t border-[var(--color-border-subtle)] pt-2">
        {secondaryItems.map((item) => (
          <SidebarNavItem key={item.label} item={item} collapsed={false} />
        ))}
      </div>
    </nav>
  );
}

export function SidebarRail() {
  return (
    <nav className="flex flex-1 flex-col items-center gap-1 overflow-y-auto px-2 py-4 custom-scrollbar" aria-label="Ana menü">
      {primaryItems.map((item) => (
        <div key={item.label} className="relative">
          <SidebarNavItem item={item} collapsed={true} />
        </div>
      ))}
      <div className="mt-auto border-t border-[var(--color-border-subtle)] pt-2 w-full flex flex-col items-center gap-1">
        {secondaryItems.map((item) => (
          <div key={item.label} className="relative">
            <SidebarNavItem item={item} collapsed={true} />
          </div>
        ))}
      </div>
    </nav>
  );
}
