import type { Metadata } from "next";
import Link from "next/link";
import UsageGuide from "@/components/UsageGuide";
import { messages } from "@/lib/messages";
import "./globals.css";

export const metadata: Metadata = {
  title: messages.app.title,
  description: messages.app.description,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <div className="app-shell">
          <header className="topbar">
            <div className="brand">
              <Link href="/" className="brand-mark">
                Skills<span>Catalog</span>
              </Link>
              <span className="brand-sub">{messages.app.brandSub}</span>
            </div>
            <nav className="nav">
              <Link href="/">{messages.nav.catalog}</Link>
              <Link href="/upload">{messages.nav.upload}</Link>
              <Link href="/git">{messages.nav.git}</Link>
              <Link href="/inquire">{messages.nav.inquire}</Link>
              <Link href="/tests">{messages.nav.tests}</Link>
              <UsageGuide />
            </nav>
          </header>
          <main className="main">{children}</main>
          <footer className="footer">{messages.app.footer}</footer>
        </div>
      </body>
    </html>
  );
}
