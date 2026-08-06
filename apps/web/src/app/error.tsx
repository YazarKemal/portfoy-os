"use client";

import { useEffect } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { ErrorState } from "@/components/ui/error-state";
import { ButtonLink } from "@/components/ui/button";

interface ErrorPageProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  useEffect(() => {
    console.error("Dashboard error:", error);
  }, [error]);

  return (
    <AppShell>
      <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto">
        <ErrorState
          title="Bir hata oluştu"
          description="Gösterge paneli yüklenirken beklenmeyen bir sorun oluştu. Lütfen tekrar deneyin."
          onRetry={reset}
          secondaryAction={
            <ButtonLink href="/" variant="tertiary">
              Ana sayfaya dön
            </ButtonLink>
          }
        />
      </div>
    </AppShell>
  );
}
