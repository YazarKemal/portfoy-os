import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Portföy OS",
  description: "Kişisel portföy takip ve karar destek sistemi",
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
