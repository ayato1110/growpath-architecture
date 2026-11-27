"use client";

import Link from "next/link";

export default function AppError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="sheet p-6 sm:p-8">
      <p className="eyebrow">Kesalahan</p>
      <h1 className="h1 mt-2">Halaman tidak dapat dimuat</h1>
      <p className="muted mt-2 max-w-[60ch]">
        Data Anda tidak berubah. Coba muat ulang halaman ini. Bila masih gagal,
        periksa koneksi ke server.
      </p>
      <div className="mt-6 flex flex-col gap-3 sm:flex-row">
        <button className="button-primary sm:w-auto" type="button" onClick={reset}>
          Coba lagi
        </button>
        <Link className="button-secondary sm:w-auto" href="/app">
          Kembali ke beranda
        </Link>
      </div>
    </div>
  );
}
