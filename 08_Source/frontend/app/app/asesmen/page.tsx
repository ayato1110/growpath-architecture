import Link from "next/link";
import { redirect } from "next/navigation";

import {
  ApiError,
  createAssessment,
  getAssessment,
  getProfileOrNull,
  listAssessments,
} from "@/lib/api";
import { getSessionToken } from "@/lib/auth";
import type { Assessment, AssessmentDetail } from "@/types/api";

import { startAssessmentAction } from "../actions";

export const dynamic = "force-dynamic";

const ASPECTS = [
  {
    code: "PSY",
    slug: "psikografi",
    name: "Psikografi",
    description: "Motif, alasan memilih bidang usaha, dan sikap terhadap risiko.",
  },
  {
    code: "PAS",
    slug: "pasar",
    name: "Pasar",
    description: "Branding, saluran penjualan, cakupan pasar, dan kesiapan bersaing.",
  },
];

export default async function AsesmenPage() {
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const profile = await getProfileOrNull(token);
  if (!profile) redirect("/app/data-usaha");

  let detail: AssessmentDetail | null = null;
  let scored: Assessment | null = null;
  let error: string | null = null;

  try {
    const list = await listAssessments(token);
    const draft = list.items.find((item) => item.status === "draft");
    if (draft) {
      detail = await getAssessment(token, draft.id);
    } else {
      scored = list.items.find((item) => item.status === "scored") ?? null;
      if (!scored) {
        const created = await createAssessment(token);
        detail = {
          assessment: created.assessment,
          criteria: created.criteria,
          answers: created.answers,
          scores: [],
          segment: null,
        };
      }
    }
  } catch (caught) {
    error =
      caught instanceof ApiError
        ? (caught.problem.detail ?? caught.problem.title)
        : "Asesmen tidak dapat dimuat.";
  }

  if (error) {
    return (
      <div className="sheet p-6 sm:p-8">
        <p className="eyebrow">Asesmen</p>
        <h1 className="h1 mt-2">Asesmen belum dapat dimulai</h1>
        <p className="muted mt-2">{error}</p>
        <Link className="button-secondary mt-6 sm:w-auto" href="/app/data-usaha">
          Periksa data usaha
        </Link>
      </div>
    );
  }

  if (!detail && scored) {
    return (
      <div className="grid gap-6">
        <header>
          <p className="eyebrow">Asesmen</p>
          <h1 className="h1 mt-2">Asesmen terakhir sudah dinilai</h1>
          <p className="muted mt-2 max-w-[60ch]">
            Skor {scored.total_score?.toFixed(1)} dari asesmen sebelumnya. Anda
            bisa membaca hasilnya atau memulai asesmen baru.
          </p>
        </header>
        <div className="flex flex-col gap-3 sm:flex-row">
          <Link
            className="button-primary sm:w-auto"
            href={`/app/hasil/${scored.id}`}
          >
            Lihat hasil
          </Link>
          <form action={startAssessmentAction}>
            <button className="button-secondary sm:w-auto" type="submit">
              Mulai asesmen baru
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (!detail) {
    return (
      <div className="sheet p-6 sm:p-8">
        <p className="eyebrow">Asesmen</p>
        <h1 className="h1 mt-2">Asesmen belum tersedia</h1>
        <p className="muted mt-2">Muat ulang halaman ini untuk mencoba lagi.</p>
      </div>
    );
  }

  const answered = new Set(
    detail.answers
      .filter((item) => item.score !== null)
      .map((item) => item.criterion_id),
  );
  const criteriaByCode = new Map<string, typeof detail.criteria>();
  for (const criterion of detail.criteria) {
    const list = criteriaByCode.get(criterion.dimension_code) ?? [];
    list.push(criterion);
    criteriaByCode.set(criterion.dimension_code, list);
  }

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Asesmen</p>
        <h1 className="h1 mt-2">Apa kondisi usaha Anda saat ini?</h1>
        <p className="muted mt-2 max-w-[60ch]">
          Dua aspek, {detail.criteria.length} pertanyaan. Jawaban tersimpan
          sebagai draf dan bisa dilanjutkan kapan saja.
        </p>
      </header>

      <div>
        <div className="flex items-baseline justify-between gap-4">
          <p className="label">
            {answered.size} dari {detail.criteria.length} pertanyaan terjawab
          </p>
          <p className="mono text-[var(--muted)]">
            {Math.round((answered.size / detail.criteria.length) * 100)}%
          </p>
        </div>
        <div className="mt-2 h-2 w-full rounded-full bg-[var(--rule)]">
          <div
            className="h-2 rounded-full bg-[var(--accent)]"
            style={{ width: `${(answered.size / detail.criteria.length) * 100}%` }}
          />
        </div>
      </div>

      <div className="grid gap-4">
        {ASPECTS.map((aspect, index) => {
          const criteria = criteriaByCode.get(aspect.code) ?? [];
          const filled = criteria.filter((item) => answered.has(item.id)).length;
          const complete = filled === criteria.length;
          return (
            <section key={aspect.code} className="sheet p-6 sm:p-8">
              <p className="eyebrow">
                Aspek {index + 1} dari {ASPECTS.length}
              </p>
              <h2 className="h2 mt-2">{aspect.name}</h2>
              <p className="muted mt-2 max-w-[60ch]">{aspect.description}</p>
              <p className="mono mt-3 text-[var(--muted)]">
                {filled} dari {criteria.length} terjawab
              </p>
              <Link
                className={
                  complete
                    ? "button-secondary mt-5 sm:w-auto"
                    : "button-primary mt-5 sm:w-auto"
                }
                href={`/app/asesmen/${detail.assessment.id}/${aspect.slug}`}
              >
                {complete
                  ? "Periksa jawaban"
                  : filled > 0
                    ? "Lanjutkan aspek"
                    : "Mulai aspek"}
              </Link>
            </section>
          );
        })}
      </div>

      <div className="flex flex-wrap gap-3">
        <Link
          className="button-secondary sm:w-auto"
          href={`/app/asesmen/${detail.assessment.id}/tinjau`}
        >
          Tinjau semua jawaban
        </Link>
      </div>
    </div>
  );
}
