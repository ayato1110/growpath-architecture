import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { getAssessment } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

import { AnswersForm } from "./answers-form";

export const dynamic = "force-dynamic";

const ASPECTS: Record<string, { code: string; name: string; next: string }> = {
  psikografi: { code: "PSY", name: "Psikografi", next: "pasar" },
  pasar: { code: "PAS", name: "Pasar", next: "tinjau" },
};

export default async function AspectPage({
  params,
}: {
  params: Promise<{ id: string; aspek: string }>;
}) {
  const { id, aspek } = await params;
  const aspect = ASPECTS[aspek];
  if (!aspect) notFound();

  const token = await getSessionToken();
  if (!token) redirect("/login");

  const detail = await getAssessment(token, id);
  if (detail.assessment.status !== "draft") {
    redirect(`/app/asesmen/${id}/tinjau`);
  }

  const criteria = detail.criteria.filter(
    (item) => item.dimension_code === aspect.code,
  );
  if (criteria.length === 0) notFound();

  const answers = new Map(
    detail.answers.map((item) => [item.criterion_id, item.raw_value]),
  );

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">
          <Link className="underline-offset-4 hover:underline" href="/app/asesmen">
            Asesmen
          </Link>{" "}
          / {aspect.name}
        </p>
        <h1 className="h1 mt-2">{aspect.name}</h1>
        <p className="muted mt-2 max-w-[60ch]">
          {criteria.length} pertanyaan. Jawaban tersimpan saat Anda menekan
          tombol di bawah.
        </p>
      </header>

      <AnswersForm
        assessmentId={id}
        dimensionCode={aspect.code}
        nextLabel={
          aspect.next === "tinjau"
            ? "Simpan dan tinjau jawaban"
            : "Simpan dan lanjut ke Pasar"
        }
        criteria={criteria}
        answers={Object.fromEntries(answers)}
      />

      <Link className="hint underline-offset-4 hover:underline" href="/app/asesmen">
        Kembali ke daftar aspek
      </Link>
    </div>
  );
}
