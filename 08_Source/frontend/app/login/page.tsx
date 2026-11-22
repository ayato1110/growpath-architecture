import { redirect } from "next/navigation";

import { getMe } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

import { LoginForm } from "./login-form";

export const dynamic = "force-dynamic";

export default async function LoginPage() {
  const token = await getSessionToken();
  const session = token ? await getMe(token).catch(() => null) : null;
  if (session) redirect("/app");

  return (
    <main className="flex min-h-dvh items-start justify-center px-5 py-10 sm:items-center sm:px-6">
      <div className="sheet w-full max-w-[420px] p-6 sm:p-8">
        <p className="brand">Growpath</p>
        <h1 className="h1 mt-4">Masuk</h1>
        <p className="muted mt-2">
          Gunakan email dan kata sandi akun Growpath Anda.
        </p>
        <LoginForm />
      </div>
    </main>
  );
}
