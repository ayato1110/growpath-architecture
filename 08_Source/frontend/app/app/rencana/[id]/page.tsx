import Link from "next/link";
import { redirect } from "next/navigation";

import { ApiError, getRoadmap } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";
import type { MilestoneStatus } from "@/types/api";

import { MilestoneForm } from "./milestone-form";

export const dynamic = "force-dynamic";

const STATUS_LABEL: Record<MilestoneStatus, string> = {
  pending: "Belum dimulai",
  in_progress: "Sedang berjalan",
  done: "Selesai",
  skipped: "Dilewati",
};

function formatDate(value: string | null): string | null {
  if (!value) return null;
  return new Date(`${value}T00:00:00Z`).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  });
}

export default async function RencanaPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const token = await getSessionToken();
  if (!token) redirect("/login");

  let roadmap;
  try {
    roadmap = await getRoadmap(token, id);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) {
      return (
        <div className="sheet p-6 sm:p-8">
          <p className="eyebrow">Rencana aksi</p>
          <h1 className="h1 mt-2">Rencana belum tersedia</h1>
          <p className="muted mt-2">
            Kirim asesmen terlebih dahulu agar tiga langkah prioritas bisa
            dibuat.
          </p>
          <Link className="button-secondary mt-6 sm:w-auto" href="/app/asesmen">
            Buka asesmen
          </Link>
        </div>
      );
    }
    throw error;
  }

  const done = roadmap.milestones.filter((item) => item.status === "done").length;

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Rencana aksi</p>
        <h1 className="h1 mt-2">Apa langkah berikutnya?</h1>
        <p className="muted mt-2 max-w-[60ch]">
          {roadmap.summary ?? "Tiga langkah prioritas dari hasil asesmen."}
        </p>
        <p className="mono mt-2 text-[var(--muted)]">
          {done} dari {roadmap.milestones.length} langkah selesai
        </p>
      </header>

      <div className="grid gap-4">
        {roadmap.milestones.map((milestone) => {
          const due = formatDate(milestone.due_date);
          const nextStatus: MilestoneStatus =
            milestone.status === "done" ? "pending" : "done";
          return (
            <section key={milestone.id} className="sheet p-6 sm:p-8">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="eyebrow">Langkah {milestone.order_no}</p>
                  <h2 className="h2 mt-1">{milestone.title}</h2>
                </div>
                <p className="label">{STATUS_LABEL[milestone.status]}</p>
              </div>

              {milestone.description ? (
                <p className="muted mt-2 max-w-[60ch]">{milestone.description}</p>
              ) : null}

              {milestone.action_items.length > 0 ? (
                <ul className="mt-4 grid list-disc gap-2 pl-5">
                  {milestone.action_items.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              ) : null}

              {due ? <p className="hint mt-4">Target: {due}</p> : null}

              <MilestoneForm
                assessmentId={id}
                milestoneId={milestone.id}
                status={nextStatus}
                label={
                  nextStatus === "done"
                    ? "Tandai selesai"
                    : "Buka kembali langkah ini"
                }
              />
            </section>
          );
        })}
      </div>

      <Link className="hint underline-offset-4 hover:underline" href={`/app/hasil/${id}`}>
        Kembali ke hasil asesmen
      </Link>
    </div>
  );
}
