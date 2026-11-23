"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

type Status = "idle" | "submitting";

export function LoginForm() {
  const router = useRouter();
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") ?? "");
    const password = String(form.get("password") ?? "");

    setStatus("submitting");
    setError(null);

    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    }).catch(() => null);

    if (!response || !response.ok) {
      const problem = response ? await response.json().catch(() => null) : null;
      setError(
        problem?.detail ??
          problem?.title ??
          "Tidak dapat menghubungi server. Pastikan backend berjalan.",
      );
      setStatus("idle");
      return;
    }

    router.replace("/app");
    router.refresh();
  }

  const submitting = status === "submitting";

  return (
    <form
      className="mt-6 grid gap-5"
      action="/api/login"
      method="post"
      onSubmit={onSubmit}
      noValidate
    >
      <div className="field">
        <label className="label" htmlFor="email">
          Email
        </label>
        <input
          className="input"
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? "login-error" : undefined}
        />
      </div>

      <div className="field">
        <label className="label" htmlFor="password">
          Kata sandi
        </label>
        <input
          className="input"
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          aria-invalid={error ? true : undefined}
          aria-describedby={error ? "login-error" : undefined}
        />
      </div>

      {error ? (
        <p className="error-text" id="login-error" role="alert">
          {error}
        </p>
      ) : null}

      <button
        className="button-primary"
        type="submit"
        disabled={submitting}
        aria-busy={submitting}
      >
        {submitting ? "Memproses…" : "Masuk"}
      </button>
    </form>
  );
}
