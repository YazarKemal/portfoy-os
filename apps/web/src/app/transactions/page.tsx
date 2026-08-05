import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { EmptyState } from "@/components/ui/empty-state";
import { Button } from "@/components/ui/button";

export default function TransactionsPage() {
  return (
    <AppShell>
      <div className="px-4 py-6 md:px-8 lg:px-10 max-w-[1600px] mx-auto">
        <PageHeader
          eyebrow="İşlemler"
          title="İşlemler"
          supporting="Alım, satım, para yatırma/çekme, temettü ve diğer işlem kayıtları"
        />
        <div className="mt-10">
          <EmptyState
            title="İşlem kaydı yakında"
            description="İşlem ekleme, listeleme ve CSV içe aktarma bir sonraki aşamada eklenecek."
            action={<Button variant="secondary">Genel Bakış&apos;a dön</Button>}
          />
        </div>
      </div>
    </AppShell>
  );
}
