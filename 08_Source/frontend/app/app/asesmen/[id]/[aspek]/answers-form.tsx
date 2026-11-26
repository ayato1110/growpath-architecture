"use client";

import { useActionState } from "react";

import type { Criterion } from "@/types/api";

import { saveAnswersAction, type FormState } from "../../../actions";

const initialState: FormState = {};

type Answers = Record<string, Record<string, unknown>>;

export function AnswersForm({
  assessmentId,
  dimensionCode,
  nextLabel,
  criteria,
  answers,
}: {
  assessmentId: string;
  dimensionCode: string;
  nextLabel: string;
  criteria: Criterion[];
  answers: Answers;
}) {
  const [state, action, pending] = useActionState(
    saveAnswersAction.bind(null, assessmentId, dimensionCode),
    initialState,
  );

  return (
    <form action={action} className="grid gap-4">
      {criteria.map((criterion) => {
        const answer = answers[String(criterion.id)] ?? {};
        return (
          <fieldset key={criterion.id} className="sheet p-6 sm:p-7">
            <legend className="px-1 text-[16px] font-medium leading-[22px]">
              {criterion.question}
            </legend>
            <input
              type="hidden"
              name="criterion_id"
              value={criterion.id}
            />
            <input
              type="hidden"
              name={`type_${criterion.id}`}
              value={criterion.input_type}
            />

            {criterion.input_type === "multi_select" ? (
              <>
                <p className="hint mt-1">Pilih semua yang sesuai.</p>
                <div className="mt-3 grid gap-1">
                  {criterion.options.map((option) => {
                    const selected = Array.isArray(answer.options)
                      ? (answer.options as string[])
                      : [];
                    return (
                      <label
                        key={option.code}
                        className="flex min-h-[44px] cursor-pointer items-center gap-3"
                      >
                        <input
                          type="checkbox"
                          name={`c_${criterion.id}`}
                          value={option.code}
                          defaultChecked={selected.includes(option.code)}
                        />
                        <span>{option.label}</span>
                      </label>
                    );
                  })}
                </div>
              </>
            ) : null}

            {criterion.input_type === "enum" || criterion.input_type === "scale" ? (
              <div className="mt-3 grid gap-1">
                {criterion.options.map((option) => (
                  <label
                    key={option.code}
                    className="flex min-h-[44px] cursor-pointer items-center gap-3"
                  >
                    <input
                      type="radio"
                      name={`c_${criterion.id}`}
                      value={option.code}
                      defaultChecked={answer.option === option.code}
                      required
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
            ) : null}

            {criterion.input_type === "number" ? (
              <div className="mt-3">
                <input
                  className="input max-w-[240px]"
                  type="number"
                  min={0}
                  name={`c_${criterion.id}`}
                  defaultValue={
                    typeof answer.value === "number" ? answer.value : ""
                  }
                  required
                />
                {criterion.unit ? (
                  <p className="hint mt-1">Satuan: {criterion.unit}</p>
                ) : null}
              </div>
            ) : null}

            {criterion.input_type === "boolean" ? (
              <div className="mt-3 grid gap-1">
                {[
                  { value: "true", label: "Ya" },
                  { value: "false", label: "Tidak" },
                ].map((option) => (
                  <label
                    key={option.value}
                    className="flex min-h-[44px] cursor-pointer items-center gap-3"
                  >
                    <input
                      type="radio"
                      name={`c_${criterion.id}`}
                      value={option.value}
                      defaultChecked={
                        answer.value === (option.value === "true")
                      }
                      required
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
            ) : null}
          </fieldset>
        );
      })}

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
          {pending ? "Menyimpan…" : nextLabel}
        </button>
      </div>
    </form>
  );
}
