import { redirect } from "next/navigation";

import { getProfileOrNull } from "@/lib/api";
import { getSessionToken } from "@/lib/auth";

import { ProfileForm } from "./profile-form";

export const dynamic = "force-dynamic";

export default async function DataUsahaPage() {
  const token = await getSessionToken();
  if (!token) redirect("/login");

  const profile = await getProfileOrNull(token);

  return (
    <div className="grid gap-6">
      <header>
        <p className="eyebrow">Data usaha</p>
        <h1 className="h1 mt-2">Data apa yang perlu Growpath ketahui?</h1>
        <p className="muted mt-2 max-w-[60ch]">
          Data ini dipakai untuk asesmen dan rencana. Skor tidak dihitung dari
          data demografi.
        </p>
      </header>

      <ProfileForm profile={profile} />
    </div>
  );
}
