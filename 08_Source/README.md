# 08_Source

Folder ini memuat kode aplikasi, struktur kerja, changelog, dan panduan menjalankan.

Status P13: pola aplikasi, struktur folder, dan branch sudah ditetapkan. Kode fitur MVP dibangun P14-P15.

## Struktur

```text
08_Source/
  frontend/       Next.js App Router dan TypeScript
  backend/        FastAPI, Pydantic v2, SQLAlchemy, Alembic
  infra/          Docker, Railway, dan script operasional
  tests/          E2E Playwright dan fixture
  docs/           Catatan implementasi
  README.md
  CHANGELOG.md
```

Dokumen lengkap: [`../03_Application/P13-App-Structure.md`](../03_Application/P13-App-Structure.md).

Folder `infra`, `tests`, dan `docs` masih placeholder. SQLAlchemy, Alembic, dan Playwright menyusul di P14.

## Branch

- `main` untuk rilis, gate, demo, dan submission.
- `dev` untuk integrasi harian. Semua pull request mengarah ke `dev`.
- `feature/<topik>` untuk fitur aplikasi.
- `docs/<topik>` untuk dokumen dan struktur.
- `hotfix/<topik>` untuk perbaikan mendesak dari `main`, lalu kembali ke `dev`.

Jangan push langsung ke `main` atau `dev`. Aturan lengkap ada di [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Batas P13 dan Session 4

P13 menetapkan pola, struktur folder, kontrak API, dan branch. Session 4 mengerjakan scaffold Next.js/FastAPI, login, role, form data usaha, health check, README cara menjalankan, tes awal, dan bukti build.

Kode fitur tidak ditulis di P13.

## Menjalankan aplikasi

Bagian ini mencakup PR14-06 dan PR14-07: kerangka aplikasi lokal, login, dan role. Fitur P14 lain belum ada di folder ini.

| Folder | Isi | Port lokal |
|---|---|---|
| `frontend/` | Next.js App Router, TypeScript, Tailwind, token DESIGN.md | 3000 |
| `backend/` | FastAPI, Pydantic v2, verifikasi JWT, CORS | 8000 |

### Prasyarat

- Node.js 20.9 atau lebih baru dan npm. Diuji pada Node 24.14.1 dan npm 11.11.0.
- Python 3.12 dan pip. Diuji pada Python 3.12.5.
- Git dan akses ke repositori ini.

### Clone

```bash
git clone https://github.com/ayato1110/growpath-architecture.git
cd growpath-architecture
git checkout dev
```

### 1. Siapkan backend

Windows (PowerShell atau Command Prompt):

```bat
cd 08_Source\backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

macOS atau Linux:

```bash
cd 08_Source/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Jalankan backend:

```bat
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

macOS atau Linux memakai `.venv/bin/python`.

Backend berhenti dengan pesan jelas bila `AUTH_MODE=local` dipakai tanpa `LOCAL_AUTH_SECRET`, tanpa `LOCAL_USERS`, atau bila `LOCAL_AUTH_SECRET` kurang dari 32 karakter. Nilainya sudah terisi di `.env.example`.

### 2. Siapkan frontend

```bat
cd 08_Source\frontend
npm install
copy .env.example .env.local
npm run dev
```

macOS atau Linux memakai `cp .env.example .env.local`.

Buka `http://localhost:3000`. Halaman `/` mengarah ke `/app`, dan `/app` mengarah ke `/login` selama belum ada sesi.

### Variabel lingkungan backend

| Variabel | Arti |
|---|---|
| `APP_ENV` | `development` saat lokal. Nilai `production` menolak `AUTH_MODE=local`. |
| `AUTH_MODE` | `local` atau `supabase`. |
| `CORS_ORIGINS` | Daftar origin dipisah koma. Hanya frontend lokal. |
| `SUPABASE_URL` | URL proyek Supabase, dipakai untuk JWKS dan login. |
| `SUPABASE_ANON_KEY` | Anon key, dipakai backend saat `AUTH_MODE=supabase`. |
| `SUPABASE_JWT_SECRET` | Opsional, cadangan HS256 untuk proyek Supabase lama. |
| `LOCAL_AUTH_SECRET` | Kunci HS256 token lokal. Ganti dengan nilai acak. |
| `LOCAL_TOKEN_TTL_MINUTES` | Umur token lokal dalam menit. |
| `LOCAL_USERS` | Daftar akun uji dalam JSON, satu objek per peran. |

### Variabel lingkungan frontend

| Variabel | Arti |
|---|---|
| `AUTH_MODE` | Harus sama dengan `AUTH_MODE` backend. |
| `BACKEND_URL` | Alamat backend, bawaan `http://127.0.0.1:8000`. |
| `NEXT_PUBLIC_SUPABASE_URL` | URL proyek Supabase untuk jalur Supabase. |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Anon key Supabase. Ini kunci publik, bukan service role. |

### Mode local untuk pengembangan

Mode ini dipakai bila kredensial Supabase belum tersedia. Isi `AUTH_MODE=local` di kedua `.env`, lalu masuk dengan salah satu akun dari `LOCAL_USERS`. Setiap akun punya email, kata sandi, peran, tenant, dan nama sendiri. Backend menolak start bila `LOCAL_USERS` kosong, ada email ganda di dalamnya, atau `LOCAL_AUTH_SECRET` kurang dari 32 karakter. Token yang diterbitkan hanya HS256 lokal, bertanda `iss=growpath-local`, dan backend menolak membuatnya saat `APP_ENV=production`.

Akun bawaan di `.env.example`, semuanya dengan kata sandi `change-me-password`:

| Email | Peran |
|---|---|
| `umkm@growpath.id` | `umkm` |
| `pendamping@growpath.id` | `pendamping` |
| `mentor@growpath.id` | `mentor` |
| `admin.b2g@growpath.id` | `admin_b2g` |
| `admin.platform@growpath.id` | `admin_platform` |

Untuk mengganti atau menambah akun, sunting array JSON di `LOCAL_USERS` lalu restart backend. Semua akun memakai tenant yang sama selama pengujian. Peran yang berbeda belum mengubah isi layar, karena fitur per peran baru ada bersama asesmen dan konsultasi.

### Mode Supabase Auth

1. Isi `NEXT_PUBLIC_SUPABASE_URL` dan `NEXT_PUBLIC_SUPABASE_ANON_KEY` di `frontend/.env.local`.
2. Isi `SUPABASE_URL` dan `SUPABASE_ANON_KEY` di `backend/.env`.
3. Set `AUTH_MODE=supabase` di kedua file.
4. Buat pengguna di Supabase Auth, lalu isi `app_metadata` pengguna dengan `tenant_id` (UUID) dan `app_role` (misalnya `umkm`). Jangan memakai kunci `role`, karena Supabase memakainya untuk peran Postgres (`authenticated`).
5. Backend memverifikasi token lewat JWKS `{SUPABASE_URL}/auth/v1/.well-known/jwks.json`. Bila proyek memakai HS256 lama, isi `SUPABASE_JWT_SECRET`.

Jalur Supabase sudah ditulis tetapi belum diuji di mesin ini karena tidak ada kredensial. Yang terbukti berjalan adalah mode local, dan bukti di `07_Evidence/PR14-06/` berasal dari mode local.

### Cek endpoint

```bash
curl http://127.0.0.1:8000/health
curl -i http://127.0.0.1:8000/auth/me
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"umkm@growpath.id","password":"change-me-password"}'
```

- `/health` mengembalikan `status`, `version`, dan `dependencies`.
- `/auth/me` tanpa token mengembalikan 401 `application/problem+json` dengan `code`.
- `/auth/login` mengembalikan `access_token`, `expires_in`, dan `user` berisi `role` serta `tenant_id`.
- `/auth/me` dengan header `Authorization: Bearer <token>` mengembalikan identitas, tenant, dan peran.

### Lint, build, dan tes

Backend:

```bat
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m ruff check .
```

Frontend:

```bat
npm run lint
npm run build
```

Tes frontend otomatis (Vitest dan Playwright sesuai TRD) belum ada. Alur login diuji manual di browser dan lewat screenshot.

### Troubleshooting

| Gejala | Penyebab dan perbaikan |
|---|---|
| `LOCAL_USERS wajib berisi minimal satu akun` | `backend/.env` belum dibuat atau `LOCAL_USERS` kosong. Salin dari `.env.example`. |
| `LOCAL_USERS memuat email ganda` | Ada email yang sama dua kali di array JSON. Hapus salah satunya. |
| UI menampilkan `Tidak dapat menghubungi server` | Backend belum jalan atau `BACKEND_URL` salah. Cek `http://127.0.0.1:8000/health`. |
| `/app` selalu kembali ke `/login` | Cookie sesi tidak ada atau token kedaluwarsa. Masuk ulang. Periksa juga `LOCAL_AUTH_SECRET` yang berubah. |
| Browser menolak permintaan dengan pesan CORS | Frontend harus dibuka dari `http://localhost:3000` atau `http://127.0.0.1:3000`, sesuai `CORS_ORIGINS`. |
| `EADDRINUSE` pada port 3000 atau 8000 | Ada proses lain di port itu. Hentikan, atau jalankan dengan port lain dan sesuaikan `BACKEND_URL` serta `CORS_ORIGINS`. |
| Build frontend gagal saat mengunduh font | `next/font/google` butuh jaringan pada build pertama. Jalankan build dengan koneksi aktif. |
| `email` ditolak saat login | Alamat email harus berbentuk valid. Domain `.test` dan `.example` ditolak validator. |

### Catatan keamanan

- `.env` dan `.env.local` tidak pernah di-commit. Yang ada di repo hanya `.env.example` dengan nilai contoh.
- Service role key hanya boleh ada di backend, tidak pernah di `NEXT_PUBLIC_*` dan tidak pernah di browser.
- Mode local hanya untuk development. Backend menolak start bila `APP_ENV=production` dengan `AUTH_MODE=local`, dan token lokal ditolak di luar mode itu.
- Token disimpan di cookie `httpOnly`, jadi JavaScript halaman tidak bisa membacanya.
- Logout menghapus cookie sesi. Pencabutan refresh token Supabase belum diimplementasikan.
- Jangan mengarahkan `CORS_ORIGINS` ke domain publik untuk mode local.

### Batas scope

Bagian menjalankan aplikasi mencakup PR14-06 dan PR14-07: aplikasi lokal dengan login, role `umkm`, route `/app` terlindungi, dan README ini. Belum ada dashboard, data usaha, asesmen, skor, konsultasi, AI, atau log. Belum ada UAT dan belum ada pengukuran SUS.

Backend menyediakan dependency `require_role` untuk endpoint yang membatasi peran. Pada PR ini endpoint yang ada, `/auth/me`, memang terbuka untuk semua peran yang sah, jadi pembatasan peran baru terpakai saat endpoint asesmen dan konsultasi datang.
