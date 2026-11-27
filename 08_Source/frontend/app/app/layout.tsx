import Link from "next/link";
import { redirect } from "next/navigation";

import { getSession } from "@/lib/auth";

export const dynamic = "force-dynamic";

const NAV = [
  { href: "/app", label: "Beranda" },
  { href: "/app/data-usaha", label: "Data usaha" },
  { href: "/app/asesmen", label: "Asesmen" },
  { href: "/app/konsultasi", label: "Konsultasi" },
  { href: "/app/log", label: "Log" },
];

export default async function AppLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  const session = await getSession();

  if (session.status === "unauthenticated") redirect("/login");

  if (session.status === "unavailable") {
    return (
      <main className="flex min-h-dvh items-start justify-center px-5 py-8 sm:items-center sm:px-6 sm:py-12">
        <div className="sheet w-full max-w-[720px] p-6 sm:p-8">
          <p className="eyebrow">Sesi</p>
          <h1 className="h1 mt-2">Sesi tidak dapat diperiksa</h1>
          <p className="muted mt-2">
            Server tidak merespons. Sesi Anda tidak dihapus. Coba lagi setelah
            backend berjalan.
          </p>
          <a className="button-secondary mt-6" href="/app">
            Coba lagi
          </a>
        </div>
      </main>
    );
  }

  return (
    <div className="min-h-dvh sm:flex">
      <aside className="hidden border-r border-[var(--border)] bg-[var(--surface)] p-5 sm:flex sm:w-[228px] sm:flex-col">
        <Link className="brand" href="/app">
          Growpath
        </Link>
        <nav aria-label="Navigasi utama" className="mt-8 grid gap-1">
          {NAV.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-[var(--radius-control)] px-3 py-2 text-[var(--text)] hover:bg-[var(--raised)]"
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <form action="/api/logout" method="post" className="mt-auto pt-8">
          <button className="button-secondary w-full" type="submit">
            Keluar
          </button>
        </form>
      </aside>

      <div className="min-w-0 flex-1">
        <header className="flex items-center justify-between border-b border-[var(--border)] bg-[var(--surface)] px-5 py-3 sm:hidden">
          <Link className="brand" href="/app">
            Growpath
          </Link>
          <form action="/api/logout" method="post">
            <button className="text-[var(--muted)]" type="submit">
              Keluar
            </button>
          </form>
        </header>
        <nav
          aria-label="Navigasi utama"
          className="flex gap-4 overflow-x-auto border-b border-[var(--border)] bg-[var(--surface)] px-5 py-3 sm:hidden"
        >
          {NAV.map((item) => (
            <Link key={item.href} href={item.href} className="whitespace-nowrap">
              {item.label}
            </Link>
          ))}
        </nav>

        <main className="mx-auto w-full max-w-[1120px] px-5 py-8 sm:px-8 sm:py-10">
          {children}
        </main>
      </div>
    </div>
  );
}
