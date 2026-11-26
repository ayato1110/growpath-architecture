import type { AuthResponse, Problem, User } from "@/types/api";

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

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
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
  return request<User>("/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
