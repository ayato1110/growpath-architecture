# Frontend

Folder ini disiapkan untuk Next.js App Router dan TypeScript.

Struktur final ada di [`../../03_Application/P13-App-Structure.md`](../../03_Application/P13-App-Structure.md).

Aturan utama:

- `app/` hanya untuk routing, layout, dan komposisi.
- `components/ui/` untuk komponen dasar.
- `components/app/` untuk komponen domain.
- `lib/api.ts` adalah satu-satunya pintu ke FastAPI.
- Browser tidak mengakses tabel Supabase langsung.

Scaffold dan implementasi dikerjakan Session 4.
