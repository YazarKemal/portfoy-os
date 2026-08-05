"use client";

import type { ReactNode } from "react";
import { IconMenu } from "@/components/ui/icons";
import { IconButton } from "@/components/ui/button";

interface TopBarProps {
  sidebarToggle?: () => void;
  children?: ReactNode;
}

export function TopBar({ sidebarToggle, children }: TopBarProps) {
  return (
    <div className="flex h-[72px] shrink-0 items-center justify-between border-b border-[var(--color-border-subtle)] bg-[var(--color-bg-surface)] px-4 md:px-6">
      <div className="flex items-center gap-3">
        {sidebarToggle && (
          <IconButton
            label="Menüyü aç"
            onClick={sidebarToggle}
            className="md:hidden"
          >
            <IconMenu size={22} />
          </IconButton>
        )}
        <span className="text-base font-semibold text-[var(--color-text-primary)] md:hidden">
          Portföy OS
        </span>
      </div>
      <div className="flex items-center gap-3">{children}</div>
    </div>
  );
}
