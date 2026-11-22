import { cookies } from "next/headers";

import { ApiError, getMe } from "@/lib/api";
import type { User } from "@/types/api";

export const SESSION_COOKIE = "growpath_session";

export type SessionState =
  | { status: "authenticated"; user: User }
  | { status: "unauthenticated" }
  | { status: "unavailable" };

export async function getSessionToken(): Promise<string | undefined> {
  return (await cookies()).get(SESSION_COOKIE)?.value;
}

export async function getSession(): Promise<SessionState> {
  const token = await getSessionToken();
  if (!token) return { status: "unauthenticated" };

  try {
    return { status: "authenticated", user: await getMe(token) };
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      return { status: "unauthenticated" };
    }
    return { status: "unavailable" };
  }
}
