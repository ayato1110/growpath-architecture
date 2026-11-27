import Link from "next/link";
import { redirect } from "next/navigation";

import { listConsultations } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

export const dynamic = "force-dynamic";

const STATUS_LABEL: Record<string, string> = {
  pending: "Menunggu",
  processing: "Diproses",
  completed: "Selesai",
  failed: "Gagal",
};

function formatDate(value: string): string {
  return new Date(value).toLocaleString("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default async function LogPage() {
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const consultations = await listConsultations(token);
  const items = consultations.items;

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Log jawaban</p>
        <h1 className="h1 mt-2">Apa yang pernah saya tanyakan?</h1>
        <p className="muted mt-2 max-w-[60ch]">
          {consultations.total} pertanyaan tersimpan. Setiap jawaban punya
          status dan sumber yang bisa diperiksa.
        </p>
      </header>

      {items.length === 0 ? (
        <section className="sheet p-6 sm:p-8">
          <p className="eyebrow">Belum ada pertanyaan</p>
          <h2 className="h2 mt-2">Mulai dari satu pertanyaan</h2>
          <p className="muted mt-2 max-w-[55ch]">
            Tanyakan hal yang paling menghambat usaha Anda. Jawaban akan
            tersimpan di sini.
          </p>
          <Link className="button-primary mt-6 sm:w-auto" href="/app/konsultasi">
            Buka konsultasi
          </Link>
        </section>
      ) : (
        <div className="grid gap-3">
          {items.map((item) => (
            <Link
              key={item.id}
              className="sheet block p-5 sm:p-6"
              href={`/app/konsultasi/${item.id}`}
            >
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <p className="label">{STATUS_LABEL[item.status] ?? item.status}</p>
                <p className="hint">{formatDate(item.created_at)}</p>
              </div>
              <p className="mt-2 line-clamp-2">{item.question}</p>
              {item.feedback ? (
                <p className="hint mt-2">
                  Umpan balik:{" "}
                  {item.feedback === "helpful" ? "berguna" : "tidak berguna"}
                </p>
              ) : null}
            </Link>
          ))}
        </div>
      )}

      <div className="flex flex-wrap gap-3">
        <Link className="button-secondary sm:w-auto" href="/app/konsultasi">
          Tanya lagi
        </Link>
      </div>
    </div>
  );
}
