import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Button } from "@/components/ui/button";

export default function PortfolioPage() {
  return (
    <AppShell>
      <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto">
        <PageHeader
          eyebrow="Portföy"
          title="Portföyüm"
          supporting="Hesaplarınız ve varlıklarınız"
        />
        <div className="mt-10">
          <EmptyState
            title="Portföy detayı yakında"
            description="Hesap ve varlık bazında detaylı portföy görünümü bir sonraki aşamada eklenecek."
            action={<Button variant="secondary">Genel Bakış&apos;a dön</Button>}
          />
        </div>
      </div>
    </AppShell>
  );
}
