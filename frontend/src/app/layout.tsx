import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Uma Analyzer",
  description: "競馬データ分析ダッシュボード"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen bg-background text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}


