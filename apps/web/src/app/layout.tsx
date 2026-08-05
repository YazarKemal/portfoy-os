import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Portföy OS — Portföy Takip ve Karar Destek",
  description:
    "Kişisel portföy takip ve açıklanabilir karar destek sistemi. Yatırımlarınızı izleyin, varlık dağılımınızı görün, işlemlerinizi kaydedin.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body className="antialiased">{children}</body>
    </html>
  );
}
