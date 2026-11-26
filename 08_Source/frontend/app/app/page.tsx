import Link from "next/link";
import { redirect } from "next/navigation";

import {
  getAssessment,
  getProfileOrNull,
  getScores,
  listAssessments,
} from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

export const dynamic = "force-dynamic";

export default async function AppHomePage() {
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const profile = await getProfileOrNull(token);
  const assessments = profile ? await listAssessments(token) : { items: [] };
  const latest = assessments.items[0];
  const detail =
    latest && latest.status === "draft"
      ? await getAssessment(token, latest.id)
      : null;
  const scores =
    latest && latest.status === "scored"
      ? await getScores(token, latest.id)
      : null;

  let stepTitle = "Lengkapi data usaha";
  let stepBody =
    "Growpath membutuhkan data dasar usaha sebelum asesmen dimulai.";
  let stepHref = "/app/data-usaha";
  let stepLabel = "Isi data usaha";

  if (profile && detail) {
    stepTitle = "Lanjutkan asesmen";
    stepBody = `${detail.answers.length} dari ${detail.criteria.length} pertanyaan sudah dijawab.`;
    stepHref = "/app/asesmen";
    stepLabel = "Lanjutkan";
  } else if (profile && scores) {
    stepTitle = "Baca hasil dan rencana";
    stepBody = `Skor ${scores.total_score.toFixed(1)} pada segmen ${scores.segment.name}. Langkah prioritas sudah tersedia.`;
    stepHref = `/app/hasil/${scores.assessment_id}`;
    stepLabel = "Lihat hasil";
  } else if (profile) {
    stepTitle = "Mulai asesmen";
    stepBody =
      "Dua aspek, dua belas pertanyaan. Skor dihitung dari jawaban Anda, bukan oleh AI.";
    stepHref = "/app/asesmen";
    stepLabel = "Mulai asesmen";
  }

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Ruang kerja</p>
        <h1 className="h1 mt-2">
          {profile ? profile.business_name : "Mulai dari data usaha"}
        </h1>
        {profile ? (
          <p className="muted mt-2">
            {profile.owner_name} · Data {profile.completeness_pct}% lengkap
          </p>
        ) : (
          <p className="muted mt-2">
            Satu kali pengisian, dipakai untuk asesmen dan rencana.
          </p>
        )}
      </header>

      <section className="sheet p-6 sm:p-8">
        <p className="eyebrow">Langkah berikutnya</p>
        <h2 className="h2 mt-2">{stepTitle}</h2>
        <p className="muted mt-2 max-w-[52ch]">{stepBody}</p>
        <Link className="button-primary mt-6 sm:w-auto" href={stepHref}>
          {stepLabel}
        </Link>
      </section>

      {scores ? (
        <section className="grid gap-4 sm:grid-cols-3">
          <div>
            <p className="eyebrow">Skor total</p>
            <p className="mt-1 text-[32px] font-semibold leading-[38px]">
              {scores.total_score.toFixed(1)}
            </p>
            <p className="muted">{scores.segment.name}</p>
          </div>
          {scores.dimensions.map((dimension) => (
            <div key={dimension.dimension_id}>
              <p className="eyebrow">{dimension.dimension_name}</p>
              <div className="mt-2 h-2 w-full rounded-full bg-[var(--rule)]">
                <div
                  className="h-2 rounded-full bg-[var(--chart-1)]"
                  style={{ width: `${Math.max(0, Math.min(100, dimension.weighted_score))}%` }}
                />
              </div>
              <p className="mono mt-1 text-[var(--muted)]">
                {dimension.weighted_score.toFixed(1)}
              </p>
            </div>
          ))}
        </section>
      ) : null}

      <section className="grid gap-3">
        <Link className="sheet block p-5" href="/app/data-usaha">
          <p className="label">Data usaha</p>
          <p className="muted mt-1">
            {profile
              ? "Perbarui identitas, kontak, dan usia usaha."
              : "Isi sepuluh data dasar usaha."}
          </p>
        </Link>
        <Link className="sheet block p-5" href="/app/asesmen">
          <p className="label">Asesmen</p>
          <p className="muted mt-1">Psikografi dan Pasar, dua belas kriteria.</p>
        </Link>
        {latest && latest.status === "scored" ? (
          <Link className="sheet block p-5" href={`/app/rencana/${latest.id}`}>
            <p className="label">Rencana aksi</p>
            <p className="muted mt-1">Tiga langkah prioritas dan statusnya.</p>
          </Link>
        ) : null}
      </section>

      <p className="hint">
        Skor dihitung dengan aturan tetap dari jawaban Anda. AI tidak menghitung
        skor.
      </p>
    </div>
  );
}
