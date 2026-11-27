# P14 · Deployment Staging Final

**Tanggal:** 27 November 2026  
**Status:** rencana final, belum dieksekusi. Eksekusi menunggu kredensial Supabase dan akun Vercel/Render.  
**Rujukan:** ADR-001 (Accepted), D-046, `P13-Hosting-Options.md`.

## 1. Pilihan final

| Komponen | Layanan | Region | Catatan |
|---|---|---|---|
| Frontend | Vercel Hobby | Singapore (fra1 terdekat) | Proyek akademik non-komersial |
| Backend | Render Free, Python 3.12 | Singapore | Tidur setelah idle; bangunkan sebelum demo |
| Database | Supabase PostgreSQL 15 + pgvector | Singapore | Session pooler port 5432 |
| AI | DeepSeek API | - | Tidak dipakai P14; disiapkan untuk P15 |
| Observability | Sentry | - | Ditambahkan setelah staging hidup |

Alur: browser → Vercel (Next.js server) → Render (FastAPI) → Supabase (PostgreSQL). Browser tidak pernah menghubungi database langsung.

## 2. Variabel lingkungan

### Render (backend)

| Variabel | Nilai staging |
|---|---|
| `APP_ENV` | `staging` |
| `AUTH_MODE` | `local` sampai Supabase Auth siap |
| `LOCAL_AUTH_SECRET` | dibuat otomatis oleh Render |
| `LOCAL_USERS` | JSON akun uji, disimpan di dashboard |
| `DATABASE_URL` | connection string Session pooler + `sslmode=require` |
| `CORS_ORIGINS` | URL produksi Vercel, tanpa garis miring di akhir |
| `DB_POOL_SIZE` | `5` |
| `DB_MAX_OVERFLOW` | `5` |
| `DEEPSEEK_API_KEY` | kosong sampai P15 |

`APP_ENV=production` menolak `AUTH_MODE=local`; karena itu staging memakai `APP_ENV=staging`.

### Vercel (frontend)

| Variabel | Nilai staging |
|---|---|
| `BACKEND_URL` | URL publik Render, misalnya `https://growpath-api.onrender.com` |
| `AUTH_MODE` | `local` |

Jangan menaruh `DATABASE_URL`, service role key, atau API key DeepSeek di frontend.

## 3. Langkah deploy

1. **Database**
   - Buat atau dapatkan project Supabase.
   - Jalankan `001_init.sql`, `seed.sql`, `002_p14.sql` lewat SQL Editor atau `psql`.
   - Verifikasi dengan `db/verify_p14.sql`.
2. **Backend**
   - Render → New → Blueprint → pilih repo → file `render.yaml` di root.
   - Isi env bertanda `sync: false`.
   - Deploy, lalu cek `GET /health` mengembalikan `status: ok`.
3. **Frontend**
   - Vercel → Add New Project → root directory `08_Source/frontend`.
   - Isi `BACKEND_URL`.
   - Deploy, lalu buka `/login`.
4. **CORS**
   - Setelah URL Vercel didapat, perbarui `CORS_ORIGINS` di Render dan redeploy.
5. **Bukti**
   - Simpan tangkapan layar health check, login, data usaha, hasil, dan rencana di `07_Evidence/P14/screenshots/`.

## 4. IP plan

Vercel, Render, dan Supabase memakai egress bersama dan **tidak memberi IP statis** pada paket gratis. Karena itu:

- Tidak ada allowlist IP untuk mitra atau kampus.
- Akses database dibatasi connection string, TLS, dan RLS, bukan IP.
- Bila institusi mensyaratkan IP tetap, opsi lanjutan adalah Cloudflare Tunnel atau paket berbayar dengan static egress. Itu di luar P14.

## 5. Checklist keamanan staging

| Kontrol | Status |
|---|---|
| HTTPS di semua domain | Bawaan Vercel dan Render |
| Rahasia hanya di dashboard, bukan repo | Wajib |
| `.env` tidak di-commit | `.gitignore` sudah menutup |
| `DATABASE_URL` memakai TLS | `sslmode=require` |
| CORS hanya origin frontend | Diisi setelah URL Vercel ada |
| Token lokal berumur 60 menit | `LOCAL_TOKEN_TTL_MINUTES=60` |
| RLS aktif di tabel | Sudah ada di `001_init.sql`; backend memakai role owner, RLS menjadi lapisan kedua |
| Tanpa service role key di browser | Wajib |
| Log tidak memuat kata sandi atau token | Periksa sebelum demo |
| Backup database | Supabase gratis tidak menyediakan backup harian; skrip backup P15 wajib sebelum UAT |

## 6. Risiko dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Render Free tidur | Buka `/health` 2 menit sebelum demo |
| Koneksi pooler menolak prepared statement | `prepare_threshold=None` sudah diset di `core/db.py` |
| Database gratis tanpa backup | Jalankan backup manual sebelum UAT; jangan pakai data nyata |
| Kuota Vercel Hobby | Proyek non-komersial; upgrade bila dikomersialkan |
| Satu role database | Buat role aplikasi terbatas di P15 bila diperlukan |

## 7. Rollback

- Frontend: Vercel → Deployments → Promote deployment sebelumnya.
- Backend: Render → Deploys → Rollback ke deploy stabil terakhir.
- Database: migrasi bersifat maju; `001_init.sql` menghapus tabel, jadi jangan dijalankan di database berisi data tanpa backup.
