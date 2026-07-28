import type { Metadata } from "next";
import Link from "next/link";
import UsageGuide from "@/components/UsageGuide";
import "./globals.css";

export const metadata: Metadata = {
  title: "Skills Catalog | ChatGPT Skills",
  description:
    "Internal catalog for registering, searching, and sharing ChatGPT Skills",
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
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"
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
              <span className="brand-sub">Internal</span>
            </div>
            <nav className="nav">
              <Link href="/">Catalog</Link>
              <Link href="/upload">Upload</Link>
              <Link href="/git">Git Sync</Link>
              <UsageGuide />
            </nav>
          </header>
          <main className="main">{children}</main>
          <footer className="footer">
            ChatGPT Skills Catalog - Internal Use Only
          </footer>
        </div>
      </body>
    </html>
  );
}
