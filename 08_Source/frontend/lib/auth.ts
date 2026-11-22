import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { getMe } from "@/lib/api";
import type { User } from "@/types/api";

export const SESSION_COOKIE = "growpath_session";

export async function getSessionToken(): Promise<string | undefined> {
  return (await cookies()).get(SESSION_COOKIE)?.value;
}

export async function requireUser(): Promise<User> {
  const token = await getSessionToken();
  const user = token ? await getMe(token).catch(() => null) : null;
  if (!user) redirect("/login");
  return user;
}
