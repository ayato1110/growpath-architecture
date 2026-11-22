import { requireUser } from "@/lib/auth";
import type { Role } from "@/types/api";

export const dynamic = "force-dynamic";

const ROLE_LABELS: Record<Role, string> = {
  umkm: "UMKM",
  pendamping: "Pendamping",
  mentor: "Mentor",
  admin_b2g: "Admin B2G",
  admin_platform: "Admin platform",
};

export default async function AppPage() {
  const user = await requireUser();

  return (
    <main className="flex min-h-dvh items-start justify-center px-5 py-8 sm:items-center sm:px-6 sm:py-12">
      <div className="sheet w-full max-w-[720px] p-6 sm:p-8">
        <p className="eyebrow">Sesi aktif</p>
        <h1 className="h1 mt-2">Akun Anda</h1>

        <dl className="mt-6 grid gap-5">
          <div className="field">
            <dt className="label">Email</dt>
            <dd className="value">{user.email}</dd>
          </div>
          <div className="field">
            <dt className="label">Peran</dt>
            <dd className="value">{ROLE_LABELS[user.role]}</dd>
          </div>
          <div className="field">
            <dt className="label">Tenant</dt>
            <dd className="value mono">{user.tenant_id}</dd>
          </div>
        </dl>

        <form action="/api/logout" method="post" className="mt-8">
          <button className="button-secondary" type="submit">
            Keluar
          </button>
        </form>
      </div>
    </main>
  );
}
