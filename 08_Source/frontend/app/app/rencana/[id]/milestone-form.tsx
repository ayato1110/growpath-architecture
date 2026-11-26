"use client";

import { useActionState } from "react";

import type { MilestoneStatus } from "@/types/api";

import { updateMilestoneAction, type FormState } from "../../actions";

const initialState: FormState = {};

export function MilestoneForm({
  assessmentId,
  milestoneId,
  status,
  label,
}: {
  assessmentId: string;
  milestoneId: string;
  status: MilestoneStatus;
  label: string;
}) {
  const [state, action, pending] = useActionState(
    updateMilestoneAction.bind(null, assessmentId),
    initialState,
  );

  return (
    <form action={action} className="mt-5">
      <input type="hidden" name="milestone_id" value={milestoneId} />
      <input type="hidden" name="status" value={status} />
      {state.error ? (
        <p className="error-text mb-2" role="alert">
          {state.error}
        </p>
      ) : null}
      <button
        className="button-secondary sm:w-auto"
        type="submit"
        disabled={pending}
        aria-busy={pending}
      >
        {pending ? "Menyimpan…" : label}
      </button>
    </form>
  );
}
