"use client";

import Link from "next/link";
import { useActionState } from "react";

import type { Profile } from "@/types/api";

import { saveProfileAction, type FormState } from "../actions";

const SECTORS: { value: string; label: string }[] = [
  { value: "kuliner", label: "Kuliner" },
  { value: "fashion", label: "Fashion" },
  { value: "kriya", label: "Kriya" },
  { value: "pertanian", label: "Pertanian" },
  { value: "perdagangan", label: "Perdagangan" },
  { value: "jasa", label: "Jasa" },
  { value: "teknologi", label: "Teknologi" },
  { value: "kesehatan", label: "Kesehatan" },
  { value: "pendidikan", label: "Pendidikan" },
  { value: "lainnya", label: "Lainnya" },
];

const GENDERS = [
  { value: "female", label: "Perempuan" },
  { value: "male", label: "Laki-laki" },
  { value: "undisclosed", label: "Tidak ingin menyebut" },
];

const initialState: FormState = {};

export function ProfileForm({ profile }: { profile: Profile | null }) {
  const [state, action, pending] = useActionState(
    saveProfileAction,
    initialState,
  );

  return (
    <form action={action} className="grid gap-6">
      {profile ? (
        <div>
          <div className="flex items-baseline justify-between gap-4">
            <p className="label">Kelengkapan data</p>
            <p className="mono text-[var(--muted)]">
              {profile.completeness_pct.toFixed(0)}%
            </p>
          </div>
          <div className="mt-2 h-2 w-full rounded-full bg-[var(--rule)]">
            <div
              className="h-2 rounded-full bg-[var(--accent)]"
              style={{ width: `${profile.completeness_pct}%` }}
            />
          </div>
        </div>
      ) : null}

      <section className="sheet grid gap-5 p-6 sm:p-8">
        <h2 className="h2">Identitas usaha</h2>

        <div className="field">
          <label className="label" htmlFor="business_name">
            Nama usaha
          </label>
          <input
            className="input"
            id="business_name"
            name="business_name"
            maxLength={160}
            required
            defaultValue={profile?.business_name ?? ""}
            aria-describedby="business_name-hint"
          />
          <p className="hint" id="business_name-hint">
            Nama yang dipakai pelanggan, bukan nama badan hukum.
          </p>
        </div>

        <div className="field">
          <label className="label" htmlFor="owner_name">
            Nama lengkap pemilik
          </label>
          <input
            className="input"
            id="owner_name"
            name="owner_name"
            maxLength={120}
            required
            defaultValue={profile?.owner_name ?? ""}
          />
        </div>

        <div className="grid gap-5 sm:grid-cols-2">
          <div className="field">
            <label className="label" htmlFor="gender">
              Jenis kelamin
            </label>
            <select
              className="input"
              id="gender"
              name="gender"
              defaultValue={profile?.gender ?? "undisclosed"}
            >
              {GENDERS.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>

          <div className="field">
            <label className="label" htmlFor="age">
              Usia
            </label>
            <input
              className="input"
              id="age"
              name="age"
              type="number"
              min={15}
              max={100}
              defaultValue={profile?.age ?? ""}
            />
            <p className="hint">Tahun, 15 sampai 100.</p>
          </div>
        </div>

        <div className="field">
          <label className="label" htmlFor="business_description">
            Deskripsi singkat usaha
          </label>
          <textarea
            className="input h-auto min-h-[96px] py-2"
            id="business_description"
            name="business_description"
            maxLength={1000}
            defaultValue={profile?.business_description ?? ""}
            aria-describedby="business_description-hint"
          />
          <p className="hint" id="business_description-hint">
            Produk utama dan siapa pembelinya. Boleh dikosongkan.
          </p>
        </div>
      </section>

      <section className="sheet grid gap-5 p-6 sm:p-8">
        <h2 className="h2">Kontak</h2>

        <div className="grid gap-5 sm:grid-cols-2">
          <div className="field">
            <label className="label" htmlFor="whatsapp">
              Nomor WhatsApp
            </label>
            <input
              className="input"
              id="whatsapp"
              name="whatsapp"
              inputMode="tel"
              defaultValue={profile?.whatsapp ?? ""}
              placeholder="0812…"
              aria-describedby="whatsapp-hint"
            />
            <p className="hint" id="whatsapp-hint">
              Format Indonesia, misalnya 081234567890.
            </p>
          </div>

          <div className="field">
            <label className="label" htmlFor="email">
              Email usaha
            </label>
            <input
              className="input"
              id="email"
              name="email"
              type="email"
              defaultValue={profile?.email ?? ""}
            />
          </div>
        </div>

        <div className="field">
          <label className="label" htmlFor="address">
            Alamat domisili
          </label>
          <textarea
            className="input h-auto min-h-[80px] py-2"
            id="address"
            name="address"
            maxLength={500}
            defaultValue={profile?.address ?? ""}
          />
        </div>
      </section>

      <section className="sheet grid gap-5 p-6 sm:p-8">
        <h2 className="h2">Sektor dan usia usaha</h2>

        <div className="field">
          <label className="label" htmlFor="sector">
            Sektor usaha
          </label>
          <select
            className="input"
            id="sector"
            name="sector"
            required
            defaultValue={profile?.sector ?? ""}
          >
            <option value="" disabled>
              Pilih sektor
            </option>
            {SECTORS.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        </div>

        <div className="grid gap-5 sm:grid-cols-2">
          <div className="field">
            <label className="label" htmlFor="established_year">
              Tahun berdiri
            </label>
            <input
              className="input"
              id="established_year"
              name="established_year"
              type="number"
              min={1900}
              max={2100}
              required
              defaultValue={profile?.established_year ?? ""}
            />
          </div>

          <div className="field">
            <label className="label" htmlFor="operation_months">
              Lama usaha (bulan)
            </label>
            <input
              className="input"
              id="operation_months"
              name="operation_months"
              type="number"
              min={0}
              max={1200}
              required
              defaultValue={profile?.operation_months ?? ""}
            />
          </div>
        </div>
      </section>

      {state.error ? (
        <p className="error-text" role="alert">
          {state.error}
        </p>
      ) : null}

      <div className="flex flex-col gap-3 sm:flex-row sm:justify-end">
        <Link className="button-secondary sm:w-auto" href="/app">
          Batal
        </Link>
        <button
          className="button-primary sm:w-auto"
          type="submit"
          disabled={pending}
          aria-busy={pending}
        >
          {pending ? "Menyimpan…" : "Simpan dan lanjut"}
        </button>
      </div>
    </form>
  );
}
