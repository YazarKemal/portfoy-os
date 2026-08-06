"use client";

import type { ReactNode } from "react";
import { useState } from "react";
import { SidebarNavigation, SidebarRail } from "./sidebar-navigation";
import { MobileNavigation } from "./mobile-navigation";
import { TopBar } from "./top-bar";

interface AppShellProps {
  children: ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="flex h-dvh overflow-hidden bg-[var(--color-bg-canvas)]">
      {/* Desktop + Tablet Sidebar */}
      <aside className="hidden md:flex md:w-20 lg:w-[248px] shrink-0 flex-col border-r border-[var(--color-border-subtle)] bg-[var(--color-bg-surface)]">
        {/* Wordmark */}
        <div className="flex h-[72px] shrink-0 items-center border-b border-[var(--color-border-subtle)] px-4">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-brand-primary)] text-[var(--color-text-inverse)] text-sm font-bold" aria-hidden="true">
              P
            </div>
            <span className="hidden lg:block text-base font-semibold text-[var(--color-text-primary)]">
              Portföy OS
            </span>
          </div>
        </div>

        {/* Desktop nav */}
        <div className="hidden lg:flex flex-1 flex-col">
          <SidebarNavigation />
        </div>

        {/* Tablet rail */}
        <div className="flex lg:hidden flex-1 flex-col">
          <SidebarRail />
        </div>
      </aside>

      {/* Main content area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <TopBar sidebarToggle={() => setMobileMenuOpen(!mobileMenuOpen)} />
        <main className="flex-1 overflow-y-auto custom-scrollbar pb-16 md:pb-0">
          {children}
        </main>
      </div>

      {/* Mobile bottom nav */}
      <MobileNavigation />

      {/* Mobile sidebar overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div
            className="absolute inset-0 bg-black/30"
            onClick={() => setMobileMenuOpen(false)}
            aria-hidden="true"
          />
          <aside className="absolute inset-y-0 left-0 w-72 bg-[var(--color-bg-surface)] shadow-lg flex flex-col">
            <div className="flex h-[72px] shrink-0 items-center border-b border-[var(--color-border-subtle)] px-4">
              <div className="flex items-center gap-2.5">
                <div className="flex h-8 w-8 items-center justify-center rounded-[var(--radius-sm)] bg-[var(--color-brand-primary)] text-[var(--color-text-inverse)] text-sm font-bold" aria-hidden="true">
                  P
                </div>
                <span className="text-base font-semibold text-[var(--color-text-primary)]">
                  Portföy OS
                </span>
              </div>
            </div>
            <SidebarNavigation />
          </aside>
        </div>
      )}
    </div>
  );
}
