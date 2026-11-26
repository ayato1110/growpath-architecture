import type {
  Assessment,
  AssessmentDetail,
  AssessmentDraft,
  AssessmentList,
  AuthResponse,
  Milestone,
  MilestoneStatus,
  Problem,
  Profile,
  ProfileInput,
  Roadmap,
  ScoreResult,
  User,
} from "@/types/api";

const API_BASE_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly problem: Problem,
  ) {
    super(problem.title);
  }
}

export function problemPayload(
  status: number,
  code: string,
  title: string,
  detail?: string,
): Problem {
  return {
    type: "about:blank",
    title,
    status,
    code,
    ...(detail ? { detail } : {}),
  };
}

function authHeaders(token?: string): Record<string, string> {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(
  path: string,
  init?: RequestInit,
  token?: string,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      ...authHeaders(token),
      ...(init?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const problem = (await response.json().catch(() => null)) as Problem | null;
    throw new ApiError(
      response.status,
      problem ??
        problemPayload(response.status, "UNKNOWN_ERROR", "Permintaan gagal"),
    );
  }

  return (await response.json()) as T;
}

export function loginWithPassword(
  email: string,
  password: string,
): Promise<AuthResponse> {
  return request<AuthResponse>("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export function getMe(token: string): Promise<User> {
  return request<User>("/auth/me", undefined, token);
}

export function getProfile(token: string): Promise<Profile> {
  return request<Profile>("/me/profile", undefined, token);
}

export async function getProfileOrNull(token: string): Promise<Profile | null> {
  try {
    return await getProfile(token);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) return null;
    throw error;
  }
}

export function saveProfile(
  token: string,
  payload: ProfileInput,
): Promise<Profile> {
  return request<Profile>(
    "/me/profile",
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
    token,
  );
}

export function listAssessments(token: string): Promise<AssessmentList> {
  return request<AssessmentList>("/assessments", undefined, token);
}

export function createAssessment(token: string): Promise<AssessmentDraft> {
  return request<AssessmentDraft>(
    "/assessments",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    },
    token,
  );
}

export function getAssessment(
  token: string,
  assessmentId: string,
): Promise<AssessmentDetail> {
  return request<AssessmentDetail>(
    `/assessments/${assessmentId}`,
    undefined,
    token,
  );
}

export function saveAnswers(
  token: string,
  assessmentId: string,
  answers: { criterion_id: number; raw_value: Record<string, unknown> }[],
): Promise<AssessmentDraft> {
  return request<AssessmentDraft>(
    `/assessments/${assessmentId}/answers`,
    {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers }),
    },
    token,
  );
}

export function submitAssessment(
  token: string,
  assessmentId: string,
): Promise<ScoreResult> {
  return request<ScoreResult>(
    `/assessments/${assessmentId}/submit`,
    { method: "POST" },
    token,
  );
}

export function getScores(
  token: string,
  assessmentId: string,
): Promise<ScoreResult> {
  return request<ScoreResult>(
    `/assessments/${assessmentId}/scores`,
    undefined,
    token,
  );
}

export function getRoadmap(
  token: string,
  assessmentId: string,
): Promise<Roadmap> {
  return request<Roadmap>(
    `/assessments/${assessmentId}/roadmap`,
    undefined,
    token,
  );
}

export function updateMilestone(
  token: string,
  milestoneId: string,
  status: MilestoneStatus,
  note?: string,
): Promise<Milestone> {
  return request<Milestone>(
    `/milestones/${milestoneId}`,
    {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, ...(note ? { note } : {}) }),
    },
    token,
  );
}

export type { Assessment };
