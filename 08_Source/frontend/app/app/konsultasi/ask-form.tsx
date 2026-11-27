"use client";

import { useActionState } from "react";

import { askConsultationAction, type FormState } from "../actions";

const initialState: FormState = {};

export function AskForm({ assessmentId }: { assessmentId: string }) {
  const [state, action, pending] = useActionState(
    askConsultationAction.bind(null, assessmentId),
    initialState,
  );

  return (
    <form action={action} className="sheet grid gap-5 p-6 sm:p-8">
      <div className="field">
        <label className="label" htmlFor="question">
          Pertanyaan
        </label>
        <textarea
          className="input h-auto min-h-[120px] py-2"
          id="question"
          name="question"
          minLength={3}
          maxLength={1000}
          required
          aria-describedby="question-hint"
          placeholder="Contoh: bagaimana cara menaikkan penjualan di marketplace?"
        />
        <p className="hint" id="question-hint">
          3 sampai 1000 karakter. Jangan tulis nomor identitas atau rekening.
        </p>
      </div>

      {state.error ? (
        <p className="error-text" role="alert">
          {state.error}
        </p>
      ) : null}

      <div className="flex justify-end">
        <button
          className="button-primary sm:w-auto"
          type="submit"
          disabled={pending}
          aria-busy={pending}
        >
          {pending ? "Menyusun jawaban…" : "Tanya"}
        </button>
      </div>
    </form>
  );
}
