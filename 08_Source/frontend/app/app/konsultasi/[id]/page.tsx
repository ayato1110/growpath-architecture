import Link from "next/link";
import { redirect } from "next/navigation";

import { ApiError, getConsultation } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

import { feedbackAction } from "../../actions";

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
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default async function KonsultasiDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = await getSessionToken();
  if (!token) redirect("/login");

  let consultation;
  try {
    consultation = await getConsultation(token, id);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return (
        <div className="sheet p-6 sm:p-8">
          <p className="eyebrow">Konsultasi</p>
          <h1 className="h1 mt-2">Pertanyaan tidak ditemukan</h1>
          <Link className="button-secondary mt-6 sm:w-auto" href="/app/log">
            Buka log
          </Link>
        </div>
      );
    }
    throw error;
  }

  const answer = consultation.answer;
  const canGiveFeedback =
    answer !== null && (answer.status === "succeeded" || answer.status === "blocked");

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Konsultasi / {STATUS_LABEL[consultation.status]}</p>
        <h1 className="h1 mt-2">Jawaban untuk pertanyaan Anda</h1>
        <p className="hint mt-2">{formatDate(consultation.created_at)}</p>
      </header>

      <section className="sheet p-6 sm:p-8">
        <p className="eyebrow">Pertanyaan</p>
        <p className="mt-2 whitespace-pre-wrap">{consultation.question}</p>
      </section>

      {answer ? (
        <section className="sheet p-6 sm:p-8">
          <p className="eyebrow">
            Jawaban {answer.status === "blocked" ? "(dibatasi)" : ""}
          </p>
          <div className="mt-2 whitespace-pre-wrap text-[16px] leading-[26px]">
            {answer.answer}
          </div>

          {answer.sources.length > 0 ? (
            <div className="mt-5">
              <p className="label">Sumber</p>
              <ul className="mt-2 grid list-disc gap-1 pl-5">
                {answer.sources.map((source, index) => (
                  <li key={`${source.source_id ?? index}`}>
                    {String(source.label ?? source.source_id ?? "Sumber")}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          <p className="hint mt-5">
            Jawaban ini disusun dari data asesmen Anda dan materi rujukan yang
            tersedia. Jawaban bisa keliru. Untuk keputusan hukum, pajak, atau
            keuangan, periksa sumber resmi atau tanyakan ke pendamping.
          </p>

          {canGiveFeedback ? (
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <p className="label">Apakah jawaban ini berguna?</p>
              <form action={feedbackAction.bind(null, id, "helpful")}>
                <button
                  className={
                    consultation.feedback === "helpful"
                      ? "button-primary sm:w-auto"
                      : "button-secondary sm:w-auto"
                  }
                  type="submit"
                >
                  Berguna
                </button>
              </form>
              <form action={feedbackAction.bind(null, id, "not_helpful")}>
                <button
                  className={
                    consultation.feedback === "not_helpful"
                      ? "button-primary sm:w-auto"
                      : "button-secondary sm:w-auto"
                  }
                  type="submit"
                >
                  Tidak berguna
                </button>
              </form>
            </div>
          ) : null}
        </section>
      ) : (
        <section className="sheet p-6 sm:p-8">
          <p className="eyebrow">Status</p>
          <h2 className="h2 mt-2">Jawaban belum tersedia</h2>
          <p className="muted mt-2">
            Pertanyaan sudah tersimpan. Coba kirim ulang dari halaman konsultasi.
          </p>
          <Link className="button-secondary mt-5 sm:w-auto" href="/app/konsultasi">
            Kembali ke konsultasi
          </Link>
        </section>
      )}

      <div className="flex flex-wrap gap-3">
        <Link className="button-secondary sm:w-auto" href="/app/konsultasi">
          Tanya lagi
        </Link>
        <Link className="button-secondary sm:w-auto" href="/app/log">
          Lihat semua log
        </Link>
      </div>
    </div>
  );
}
