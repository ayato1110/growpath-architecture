import Link from "next/link";
import { redirect } from "next/navigation";

import { getProfileOrNull, listAssessments } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

import { AskForm } from "./ask-form";

export const dynamic = "force-dynamic";

export default async function KonsultasiPage() {
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const profile = await getProfileOrNull(token);
  if (!profile) redirect("/app/data-usaha");

  const assessments = await listAssessments(token);
  const scored = assessments.items.find((item) => item.status === "scored");

  if (!scored) {
    return (
      <div className="sheet p-6 sm:p-8">
        <p className="eyebrow">Konsultasi</p>
        <h1 className="h1 mt-2">Selesaikan asesmen dulu</h1>
        <p className="muted mt-2 max-w-[60ch]">
          Konsultasi memakai skor, segmen, dan prioritas dari asesmen yang sudah
          dinilai.
        </p>
        <Link className="button-secondary mt-6 sm:w-auto" href="/app/asesmen">
          Buka asesmen
        </Link>
      </div>
    );
  }

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Konsultasi</p>
        <h1 className="h1 mt-2">Apa yang bisa saya tanyakan?</h1>
        <p className="muted mt-2 max-w-[60ch]">
          Pertanyaan dijawab dari data usaha, hasil asesmen, dan prioritas Anda.
          Skor tetap dihitung sistem, bukan oleh AI.
        </p>
      </header>

      <AskForm assessmentId={scored.id} />

      <p className="hint max-w-[70ch]">
        Jawaban ini disusun dari data asesmen Anda dan materi rujukan yang
        tersedia. Jawaban bisa keliru. Untuk keputusan hukum, pajak, atau
        keuangan, periksa sumber resmi atau tanyakan ke pendamping.
      </p>

      <Link className="hint underline-offset-4 hover:underline" href="/app/log">
        Lihat log pertanyaan
      </Link>
    </div>
  );
}
