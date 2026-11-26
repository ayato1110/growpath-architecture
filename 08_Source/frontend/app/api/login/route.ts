import { createClient } from "@supabase/supabase-js";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { ApiError, loginWithPassword, problemPayload } from "@/lib/api";
import { SESSION_COOKIE } from "@/lib/auth";

const AUTH_MODE = process.env.AUTH_MODE ?? "local";

type Credentials = { email: string; password: string };
type Session = { access_token: string; expires_in: number };

export async function POST(request: Request) {
  const credentials = await readCredentials(request);

  if (!credentials) {
    return problemResponse(
      422,
      "VALIDATION_FAILED",
      "Data masuk tidak lengkap",
      "Email dan kata sandi wajib diisi.",
    );
  }

  try {
    const session =
      AUTH_MODE === "supabase"
        ? await signInWithSupabase(credentials)
        : await loginWithPassword(credentials.email, credentials.password);

    (await cookies()).set(SESSION_COOKIE, session.access_token, {
      httpOnly: true,
      maxAge: session.expires_in,
      path: "/",
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
    });

    return NextResponse.json({ ok: true });
  } catch (error) {
    if (error instanceof ApiError) {
      return problemResponse(
        error.status,
        error.problem.code,
        error.problem.title,
        error.problem.detail,
      );
    }
    return problemResponse(
      502,
      "AUTH_UPSTREAM_UNAVAILABLE",
      "Layanan autentikasi tidak tersedia",
      "Coba lagi beberapa saat lagi.",
    );
  }
}

async function readCredentials(request: Request): Promise<Credentials | null> {
  try {
    const body = await request.json();
    const email = typeof body?.email === "string" ? body.email.trim() : "";
    const password = typeof body?.password === "string" ? body.password : "";
    return email && password ? { email, password } : null;
  } catch {
    return null;
  }
}

async function signInWithSupabase({
  email,
  password,
}: Credentials): Promise<Session> {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !anonKey) {
    throw new ApiError(
      500,
      problemPayload(
        500,
        "CONFIG_MISSING",
        "Konfigurasi Supabase belum diisi",
        "Isi NEXT_PUBLIC_SUPABASE_URL dan NEXT_PUBLIC_SUPABASE_ANON_KEY.",
      ),
    );
  }

  const supabase = createClient(url, anonKey, {
    auth: { persistSession: false, autoRefreshToken: false },
  });
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error || !data.session) {
    throw new ApiError(
      401,
      problemPayload(
        401,
        "AUTH_INVALID_CREDENTIALS",
        "Kredensial tidak valid",
        "Email atau kata sandi salah.",
      ),
    );
  }

  return {
    access_token: data.session.access_token,
    expires_in: data.session.expires_in,
  };
}

function problemResponse(
  status: number,
  code: string,
  title: string,
  detail?: string,
) {
  return NextResponse.json(problemPayload(status, code, title, detail), {
    status,
  });
}
