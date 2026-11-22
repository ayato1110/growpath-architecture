# POLA APLIKASI DAN STRUKTUR FOLDER GROWPATH

> Dokumen repo: salinan dari `APP-DEV/p13/app-structure.md`. Path kode mengikuti `08_Source/`.

**Deliverable:** P13-12 dan P13-13
**Pemilik:** Bagas Adinata
**Status:** Final P13 untuk pola dan struktur. Implementasi kode di Session 4.
**Berlaku:** P13-P16
**Keputusan terkait:** D-018, S2-2B-07, S2-2B-08
**Sumber:** `TRD.md` bagian 4, `P13-P16-HANDOFF.md`, `CONTRIBUTING.md`

## 1. Keputusan

1. Kode aplikasi berada di satu monorepo: `ARCHITECTURE_REPOSITORY/08_Source`. Jangan membuat repo aplikasi terpisah.
2. Frontend memakai Next.js App Router dan TypeScript. Route file tipis; logika domain tidak ditulis di `page.tsx`.
3. Backend memakai FastAPI dan Pydantic v2 dengan lapisan `api`, `schemas`, `services`, `repositories`, dan `models`.
4. Database, auth, dan storage memakai Supabase. Browser hanya memakai anon key untuk auth dan API; service role key hanya di backend.
5. Semua mutasi data lewat FastAPI. Server action, bila dipakai, hanya memanggil FastAPI, bukan menulis tabel langsung.
6. Kontrak API memakai OpenAPI di `03_Application/openapi.yaml`. Tipe frontend mengikuti kontrak itu.
7. Skor dihitung deterministic di `services/scoring.py`. AI hanya di `services/ai.py`; router tidak memanggil model langsung.
8. Branch: `main` untuk rilis, `dev` untuk integrasi, `feature/*` atau `docs/*` untuk pekerjaan. Semua perubahan masuk `dev` lewat pull request.
9. P13 hanya menetapkan pola, struktur folder, dan branch. Scaffold, login, role, dan README menjalankan dikerjakan Session 4.

## 2. Pohon folder

```text
08_Source/
  frontend/
    app/
      (auth)/
        login/page.tsx
        register/page.tsx
        reset-password/page.tsx
      (app)/
        layout.tsx
        dashboard/page.tsx
        profile/page.tsx
        assessment/[aspect]/page.tsx
        assessment/review/page.tsx
        results/page.tsx
        plan/page.tsx
        consultation/page.tsx
        logs/page.tsx
        logs/[id]/page.tsx
      layout.tsx
      page.tsx
    components/
      ui/
      app/
    lib/
      api.ts
      auth.ts
      format.ts
      supabase-browser.ts
    styles/
      tokens.css
      globals.css
    types/
      api.ts
    public/
    .env.example
  backend/
    app/
      main.py
      api/
        v1/
          router.py
          auth.py
          profile.py
          assessments.py
          results.py
          plans.py
          consultations.py
          logs.py
          dashboard.py
      core/
        config.py
        security.py
        errors.py
      models/
      schemas/
      services/
        scoring.py
        recommendation.py
        ai.py
      repositories/
      dependencies.py
    alembic/
      versions/
      env.py
    tests/
      conftest.py
      test_scoring.py
      test_guardrails.py
      test_api_contract.py
    pyproject.toml
    .env.example
  infra/
    docker/
    railway/
    scripts/
  tests/
    e2e/
      login.spec.ts
      assessment.spec.ts
      consultation.spec.ts
    fixtures/
  docs/
    README.md
  README.md
  CHANGELOG.md
```

## 3. Aturan frontend

- `app/` hanya untuk routing, layout, dan komposisi.
- `(auth)` memuat login, daftar, dan reset kata sandi.
- `(app)` memuat layar setelah login dan memakai shell aplikasi.
- `components/ui/` untuk tombol, input, label, card, progress, dialog, dan empty state.
- `components/app/` untuk komponen domain seperti form data usaha, kartu aspek, ringkasan skor, dan baris log.
- `lib/api.ts` adalah satu-satunya pintu ke FastAPI.
- `lib/auth.ts` mengelola sesi Supabase dan pengambilan JWT.
- `lib/supabase-browser.ts` hanya memakai URL dan anon key.
- `styles/tokens.css` memuat token warna, jarak, radius, dan tipografi. Tidak ada warna hardcode di komponen.
- `types/api.ts` mengikuti OpenAPI. Jangan menduplikasi tipe respons di banyak file.
- Jangan mengakses tabel Supabase langsung dari browser.
- Jangan menaruh `SUPABASE_SERVICE_ROLE_KEY` di `NEXT_PUBLIC_*`.

## 4. Aturan backend

- `api/v1/` hanya menangani HTTP: validasi request, dependency, status code, dan pemanggilan service.
- `schemas/` memuat model Pydantic request dan response.
- `services/` memuat aturan bisnis: skor, rekomendasi, konsultasi, guardrail, dan kuota.
- `repositories/` adalah satu-satunya lapisan yang mengakses database.
- `models/` memuat model SQLAlchemy 2.x.
- `core/config.py` memuat setting dari environment.
- `core/security.py` memverifikasi JWT Supabase dan mengambil `tenant_id` serta `user_id`.
- `core/errors.py` memetakan error domain ke respons HTTP yang konsisten.
- `dependencies.py` menyediakan sesi database, pengguna aktif, dan pemeriksaan role.
- `tenant_id` diambil dari sesi/JWT, bukan dari body request.
- `alembic/` mengelola migrasi. DDL dari Wisnu menjadi acuan skema; jangan memakai auto-create tabel di production.
- Router tidak memanggil model AI langsung. Guardrail dan kuota wajib lewat `services/ai.py`.
- Jangan mengembalikan traceback, SQL, atau data pribadi ke klien.

## 5. Alur auth dan data

```text
Browser
  -> Supabase Auth (login, daftar, reset)
  -> JWT
  -> Next.js server/client
  -> FastAPI dengan Bearer JWT
  -> verifikasi JWT dan tenant
  -> service
  -> repository
  -> PostgreSQL Supabase
```

Aturan:

- Supabase Auth hanya untuk identitas dan sesi.
- Data usaha, asesmen, skor, rencana, konsultasi, dan log selalu lewat FastAPI.
- Frontend tidak menyimpan service role key.
- Setiap query data memakai `tenant_id` dan `user_id` dari pengguna aktif.
- Endpoint yang membutuhkan role memakai dependency yang sama, bukan pengecekan tersebar di router.

## 6. Testing

- `backend/tests/` memakai Pytest untuk skor, guardrail, repository, dan kontrak API.
- `frontend` memakai Vitest untuk fungsi format dan komponen kritis.
- `tests/e2e/` memakai Playwright untuk login, data usaha, asesmen, hasil, konsultasi, log, dan dashboard.
- Tes skor ditulis sebelum UI skor dihubungkan.
- Tes guardrail memakai kasus probe dan status `blocked`.
- Jangan mengklaim UAT atau SUS dari tes otomatis.

## 7. Environment

Frontend:

```text
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
NEXT_PUBLIC_API_BASE_URL
```

Backend:

```text
SUPABASE_URL
SUPABASE_JWT_SECRET
SUPABASE_SERVICE_ROLE_KEY
DATABASE_URL
GEMINI_API_KEY
SENTRY_DSN
```

- Hanya nama variabel yang masuk `.env.example`.
- `.env` tidak pernah di-commit.
- Rahasia disimpan di Railway dan Supabase.
- `SUPABASE_SERVICE_ROLE_KEY` dan `GEMINI_API_KEY` hanya di backend.

## 8. Penamaan

- Route dan folder URL: `kebab-case`.
- Komponen React: `PascalCase`.
- Fungsi dan variabel TypeScript: `camelCase`.
- File Python: `snake_case`.
- Tabel dan kolom database: `snake_case`.
- Tipe API: `PascalCase` dengan akhiran `Request` atau `Response`.
- Satu file satu tanggung jawab utama.

## 9. Branch dan pull request

| Branch | Fungsi |
|---|---|
| `main` | Versi stabil untuk gate, demo, dan submission |
| `dev` | Integrasi harian dan target semua PR |
| `feature/<topik>` | Fitur aplikasi |
| `docs/<topik>` | Dokumen dan struktur |
| `hotfix/<topik>` | Perbaikan mendesak dari `main`, lalu kembali ke `dev` |

Aturan:

1. Jangan push langsung ke `main` atau `dev`.
2. Buat branch dari `dev` terbaru.
3. Satu PR satu topik.
4. PR selalu ke `dev`, bukan `main`.
5. Minimal satu reviewer; code owner wajib bila diatur.
6. Jangan commit `.env`, token, password, atau data pribadi.
7. Hapus branch setelah merge.
8. `main` hanya diperbarui lewat PR rilis dari `dev`.

## 10. Batas P13 dan Session 4

Sudah diputuskan di P13:

- Pola aplikasi.
- Struktur folder.
- Branch `main`, `dev`, `feature/*`.
- Batas frontend, backend, dan Supabase.
- Kontrak API sebagai acuan tipe.

Dikerjakan Session 4:

- Scaffold Next.js dan FastAPI.
- Login, daftar, reset kata sandi, dan role.
- Form data usaha.
- Health check.
- README cara menjalankan.
- Tes awal dan bukti build.

Jangan menulis kode fitur di P13. Dokumen ini adalah kontrak kerja untuk Session 4.
