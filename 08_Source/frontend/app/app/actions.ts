"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import {
  ApiError,
  createAssessment,
  createConsultation,
  saveAnswers,
  saveProfile,
  sendFeedback,
  submitAssessment,
  updateMilestone,
} from "@/lib/api";
import { getSessionToken } from "@/lib/auth";
import type {
  FeedbackValue,
  MilestoneStatus,
  ProfileInput,
} from "@/types/api";

export type FormState = { error?: string; ok?: boolean };

function messageOf(error: unknown): string {
  if (error instanceof ApiError) {
    return error.problem.detail ?? error.problem.title;
  }
  return "Tidak dapat menghubungi server. Coba lagi.";
}

async function requireToken(): Promise<string> {
  const token = await getSessionToken();
  if (!token) redirect("/login");
  return token;
}

function text(formData: FormData, name: string): string {
  return String(formData.get(name) ?? "").trim();
}

function optionalText(formData: FormData, name: string): string | null {
  const value = text(formData, name);
  return value === "" ? null : value;
}

function optionalNumber(formData: FormData, name: string): number | null {
  const value = text(formData, name);
  if (value === "") return null;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export async function saveProfileAction(
  _state: FormState,
  formData: FormData,
): Promise<FormState> {
  const token = await requireToken();
  const gender = text(formData, "gender");
  const payload: ProfileInput = {
    business_name: text(formData, "business_name"),
    owner_name: text(formData, "owner_name"),
    gender:
      gender === "male" || gender === "female" || gender === "undisclosed"
        ? gender
        : null,
    age: optionalNumber(formData, "age"),
    whatsapp: optionalText(formData, "whatsapp")?.replace(/[\s-]/g, "") ?? null,
    email: optionalText(formData, "email"),
    address: optionalText(formData, "address"),
    sector: text(formData, "sector") as ProfileInput["sector"],
    established_year: Number(text(formData, "established_year")),
    operation_months: Number(text(formData, "operation_months")),
    business_description: optionalText(formData, "business_description"),
  };

  try {
    await saveProfile(token, payload);
  } catch (error) {
    return { error: messageOf(error) };
  }
  redirect("/app/asesmen");
}

export async function startAssessmentAction(): Promise<void> {
  const token = await requireToken();
  await createAssessment(token);
  redirect("/app/asesmen");
}

export async function saveAnswersAction(
  assessmentId: string,
  dimensionCode: string,
  _state: FormState,
  formData: FormData,
): Promise<FormState> {
  const token = await requireToken();
  const criterionIds = formData.getAll("criterion_id").map(Number);
  const answers: { criterion_id: number; raw_value: Record<string, unknown> }[] = [];

  for (const criterionId of criterionIds) {
    const inputType = String(formData.get(`type_${criterionId}`) ?? "");
    const field = `c_${criterionId}`;
    if (inputType === "multi_select") {
      answers.push({
        criterion_id: criterionId,
        raw_value: { options: formData.getAll(field).map(String) },
      });
    } else if (inputType === "number") {
      answers.push({
        criterion_id: criterionId,
        raw_value: { value: Number(formData.get(field)) },
      });
    } else if (inputType === "boolean") {
      answers.push({
        criterion_id: criterionId,
        raw_value: { value: String(formData.get(field)) === "true" },
      });
    } else {
      answers.push({
        criterion_id: criterionId,
        raw_value: { option: String(formData.get(field) ?? "") },
      });
    }
  }

  try {
    await saveAnswers(token, assessmentId, answers);
  } catch (error) {
    return { error: messageOf(error) };
  }
  redirect(
    dimensionCode === "PSY"
      ? `/app/asesmen/${assessmentId}/pasar`
      : `/app/asesmen/${assessmentId}/tinjau`,
  );
}

export async function submitAssessmentAction(
  assessmentId: string,
): Promise<FormState> {
  const token = await requireToken();
  try {
    await submitAssessment(token, assessmentId);
  } catch (error) {
    return { error: messageOf(error) };
  }
  redirect(`/app/hasil/${assessmentId}`);
}

export async function updateMilestoneAction(
  assessmentId: string,
  _state: FormState,
  formData: FormData,
): Promise<FormState> {
  const token = await requireToken();
  const milestoneId = text(formData, "milestone_id");
  const status = text(formData, "status") as MilestoneStatus;
  try {
    await updateMilestone(token, milestoneId, status);
  } catch (error) {
    return { error: messageOf(error) };
  }
  revalidatePath(`/app/rencana/${assessmentId}`);
  return { ok: true };
}


export async function askConsultationAction(
  assessmentId: string,
  _state: FormState,
  formData: FormData,
): Promise<FormState> {
  const token = await requireToken();
  const question = text(formData, "question");
  let consultation;
  try {
    consultation = await createConsultation(token, assessmentId, question);
  } catch (error) {
    if (error instanceof ApiError && error.status === 503) {
      return {
        error: "Layanan AI belum siap. Coba lagi setelah konfigurasi selesai.",
      };
    }
    return { error: messageOf(error) };
  }
  redirect(`/app/konsultasi/${consultation.id}`);
}

export async function feedbackAction(
  consultationId: string,
  value: FeedbackValue,
): Promise<void> {
  const token = await requireToken();
  await sendFeedback(token, consultationId, value);
  revalidatePath(`/app/konsultasi/${consultationId}`);
  revalidatePath("/app/log");
}
