# ADR-002 Pola Aplikasi, Struktur Folder, dan Branch

- Status: Accepted untuk P13.
- Tanggal: 22 November 2026.
- Pemilik: Bagas Adinata.
- Peninjau: Ripa Bagaskara, Wisnu Nugroho.
- Rujukan: `03_Application/P13-App-Structure.md`, `CONTRIBUTING.md`, `TRD.md` bagian 4.

## Konteks

P13 membutuhkan pola aplikasi dan struktur folder yang bisa langsung dipakai P14. Repositori sudah memakai branch `main`, `dev`, dan branch fitur. Kerangka Next.js/FastAPI, login, role, health check, dan README sudah masuk; fitur MVP menyusul.

## Keputusan

- Kode aplikasi berada di satu monorepo `08_Source`.
- Frontend memakai Next.js App Router dan TypeScript.
- Backend memakai FastAPI dan Pydantic v2 dengan lapisan `api`, `schemas`, `services`, `repositories`, dan `models`.
- Database, auth, dan storage memakai Supabase.
- Browser hanya memakai anon key. Service role key dan API key AI hanya di backend.
- Semua mutasi data lewat FastAPI. Server action hanya memanggil FastAPI, bukan menulis tabel langsung.
- `tenant_id` dan `user_id` diambil dari JWT, bukan dari body request.
- OpenAPI menjadi kontrak tipe frontend.
- Branch `main` untuk rilis, `dev` untuk integrasi, `feature/*` atau `docs/*` untuk pekerjaan.
- Scaffold, login, role, health check, dan README cara menjalankan sudah masuk pada implementasi P14.

## Konsekuensi

- P14 harus mengikuti struktur dan batas lapisan ini.
- Frontend tidak boleh mengakses tabel Supabase langsung.
- Setiap endpoint baru harus masuk kontrak OpenAPI.
- Setiap perubahan masuk `dev` lewat pull request, bukan push langsung.
- Folder `08_Source/frontend`, `backend`, `infra`, `tests`, dan `docs` menjadi titik mulai P14.

## Alternatif yang ditolak

- Repo aplikasi terpisah dari `ARCHITECTURE_REPOSITORY`.
- Frontend mengakses tabel Supabase langsung.
- Logika skor atau AI di route handler.
- Push langsung ke `main` atau `dev`.
- Menulis kode fitur di P13 sebelum struktur dan kontrak disetujui.
