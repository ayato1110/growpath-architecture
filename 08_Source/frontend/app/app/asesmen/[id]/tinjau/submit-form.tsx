"use client";

import { useActionState } from "react";

import { submitAssessmentAction, type FormState } from "../../../actions";

const initialState: FormState = {};

export function SubmitForm({
  assessmentId,
  disabled,
  remaining,
}: {
  assessmentId: string;
  disabled: boolean;
  remaining: number;
}) {
  const [state, action, pending] = useActionState(
    submitAssessmentAction.bind(null, assessmentId),
    initialState,
  );

  return (
    <form action={action} className="grid gap-3">
      {state.error ? (
        <p className="error-text" role="alert">
          {state.error}
        </p>
      ) : null}
      {disabled ? (
        <p className="hint">
          Lengkapi {remaining} pertanyaan yang tersisa untuk menghitung skor.
        </p>
      ) : null}
      <div className="flex justify-end">
        <button
          className="button-primary sm:w-auto"
          type="submit"
          disabled={disabled || pending}
          aria-busy={pending}
        >
          {pending ? "Menghitung…" : "Hitung skor"}
        </button>
      </div>
    </form>
  );
}
