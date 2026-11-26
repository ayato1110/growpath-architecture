import Link from "next/link";
import { redirect } from "next/navigation";

import { ApiError, getAssessment, getRoadmap, getScores } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";
import type { Roadmap } from "@/types/api";

export const dynamic = "force-dynamic";

export default async function HasilPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const detail = await getAssessment(token, id);
  if (detail.assessment.status !== "scored") {
    redirect(`/app/asesmen/${id}/tinjau`);
  }

  const scores = await getScores(token, id);
  let roadmap: Roadmap | null = null;
  try {
    roadmap = await getRoadmap(token, id);
  } catch (error) {
    if (!(error instanceof ApiError && error.status === 404)) throw error;
  }

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Hasil asesmen</p>
        <h1 className="h1 mt-2">Di mana posisi usaha saya?</h1>
      </header>

      <section className="sheet p-6 sm:p-8">
        <p className="eyebrow">Skor total</p>
        <p className="mt-2 text-[40px] font-semibold leading-[46px]">
          {scores.total_score.toFixed(1)}
        </p>
        <p className="h2 mt-1">{scores.segment.name}</p>
        <p className="muted mt-2 max-w-[60ch]">
          Segmen dihitung dari skor total dengan ambang 0, 30, 55, dan 80.
          Batas bawah termasuk dalam segmen.
        </p>
        <p className="hint mt-3">
          {scores.criteria_answered} dari {scores.criteria_total} kriteria
          dinilai. P14 menilai aspek Psikografi dan Pasar; aspek lain menyusul.
        </p>
      </section>

      <section className="sheet p-6 sm:p-8">
        <h2 className="h2">Skor per aspek</h2>
        <div className="mt-5 grid gap-5">
          {scores.dimensions.map((dimension) => (
            <div key={dimension.dimension_id}>
              <div className="flex items-baseline justify-between gap-4">
                <p className="label">{dimension.dimension_name}</p>
                <p className="mono text-[var(--muted)]">
                  {dimension.weighted_score.toFixed(1)}
                </p>
              </div>
              <div className="mt-2 h-2 w-full rounded-full bg-[var(--rule)]">
                <div
                  className="h-2 rounded-full bg-[var(--chart-1)]"
                  style={{
                    width: `${Math.max(
                      0,
                      Math.min(100, dimension.weighted_score),
                    )}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      {roadmap ? (
        <section className="sheet p-6 sm:p-8">
          <p className="eyebrow">Tiga area prioritas</p>
          <h2 className="h2 mt-2">{roadmap.title}</h2>
          <p className="muted mt-2 max-w-[60ch]">{roadmap.summary}</p>
          <ol className="mt-5 grid gap-3">
            {roadmap.milestones.map((milestone) => (
              <li key={milestone.id} className="flex gap-3">
                <span className="mono text-[var(--muted)]">
                  {milestone.order_no}.
                </span>
                <span>{milestone.title}</span>
              </li>
            ))}
          </ol>
        </section>
      ) : null}

      <div className="flex flex-col gap-3 sm:flex-row">
        {roadmap ? (
          <Link
            className="button-primary sm:w-auto"
            href={`/app/rencana/${id}`}
          >
            Lihat rencana aksi
          </Link>
        ) : null}
        <Link className="button-secondary sm:w-auto" href="/app">
          Kembali ke beranda
        </Link>
      </div>

      <p className="hint">
        Skor dihitung dengan aturan tetap dari jawaban Anda. AI tidak menghitung
        skor.
      </p>
    </div>
  );
}
