import Link from "next/link";
import { redirect } from "next/navigation";

import { getAssessment } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";
import type { AssessmentAnswer, Criterion } from "@/types/api";

import { SubmitForm } from "./submit-form";

export const dynamic = "force-dynamic";

function answerLabel(criterion: Criterion, answer?: AssessmentAnswer): string {
  if (!answer) return "Belum dijawab";
  const raw = answer.raw_value;
  if (Array.isArray(raw.options)) {
    const codes = raw.options as string[];
    return codes
      .map(
        (code) =>
          criterion.options.find((option) => option.code === code)?.label ?? code,
      )
      .join(", ");
  }
  if (typeof raw.option === "string") {
    return (
      criterion.options.find((option) => option.code === raw.option)?.label ??
      raw.option
    );
  }
  if (typeof raw.value === "boolean") return raw.value ? "Ya" : "Tidak";
  if (typeof raw.value === "number") {
    return `${raw.value}${criterion.unit ? ` ${criterion.unit}` : ""}`;
  }
  return "Terjawab";
}

export default async function TinjauPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const detail = await getAssessment(token, id);
  if (detail.assessment.status !== "draft") {
    redirect(`/app/hasil/${id}`);
  }

  const answers = new Map(
    detail.answers.map((item) => [item.criterion_id, item]),
  );
  const unanswered = detail.criteria.filter(
    (criterion) => !answers.get(criterion.id)?.score,
  );
  const dimensions = Array.from(
    new Map(
      detail.criteria.map((criterion) => [criterion.dimension_code, criterion]),
    ).values(),
  );

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Asesmen / Tinjau jawaban</p>
        <h1 className="h1 mt-2">Periksa jawaban sebelum menghitung skor</h1>
        <p className="muted mt-2 max-w-[60ch]">
          {detail.criteria.length - unanswered.length} dari{" "}
          {detail.criteria.length} pertanyaan terjawab. Skor dihitung dari
          jawaban ini dengan aturan tetap, bukan oleh AI.
        </p>
      </header>

      {unanswered.length > 0 ? (
        <p className="error-text" role="status">
          Masih ada {unanswered.length} pertanyaan belum dijawab. Lengkapi dulu
          sebelum menghitung skor.
        </p>
      ) : null}

      {dimensions.map((dimension) => {
        const criteria = detail.criteria.filter(
          (criterion) => criterion.dimension_code === dimension.dimension_code,
        );
        const slug = dimension.dimension_code === "PSY" ? "psikografi" : "pasar";
        return (
          <section key={dimension.dimension_code} className="sheet p-6 sm:p-8">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="h2">{dimension.dimension_name}</h2>
              <Link
                className="button-secondary sm:w-auto"
                href={`/app/asesmen/${id}/${slug}`}
              >
                Ubah
              </Link>
            </div>
            <dl className="mt-4 grid gap-4">
              {criteria.map((criterion) => (
                <div key={criterion.id}>
                  <dt className="label">{criterion.question}</dt>
                  <dd
                    className={
                      answers.get(criterion.id)?.score
                        ? "value mt-1"
                        : "value mt-1 text-[var(--negative)]"
                    }
                  >
                    {answerLabel(criterion, answers.get(criterion.id))}
                  </dd>
                </div>
              ))}
            </dl>
          </section>
        );
      })}

      <SubmitForm
        assessmentId={id}
        disabled={unanswered.length > 0}
        remaining={unanswered.length}
      />
    </div>
  );
}
