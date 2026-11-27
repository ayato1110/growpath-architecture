# P14 · Gate 2 Build Review Checklist

**Tanggal:** 27 November 2026  
**Status keseluruhan:** **Siap demo lokal** — database Supabase aktif; staging Render/Vercel dan demo kelas belum.  
**Aturan:** jangan menandai butir lulus tanpa bukti eksekusi.

## Definition of Done dosen

| No | Butir | Status | Bukti yang sudah ada | Kekurangan |
|---:|---|---|---|---|
| 1 | Demo langsung 2 fitur Must end-to-end dengan database nyata | Terbukti lokal + Supabase | `smoke-report.json`, 14 screenshot, `db-verify.txt` | Demo tatap muka di kelas |
| 2 | ADR tech stack tertulis dan disetujui CEO | Lulus | `06_Governance/ADR-001-tech-stack.md`, Accepted 27 November 2026 | - |
| 3 | Topologi + deployment diagram final, versi awal ter-deploy ke staging | Sebagian | Database Supabase aktif; `04_Technology/P14-Staging-Deployment.md`, `render.yaml` | Deploy backend Render dan frontend Vercel |
| 4 | Change Request dari Kartu Kejutan terdokumentasi dengan keputusan | Belum | `06_Governance/CHANGE-REQUEST-LOG.md` | CR dari skenario kelas belum ada |
| 5 | Tidak ada anggota dengan nol kontribusi | Lulus | `07_Evidence/P14/CONTRIBUTION-AUDIT.md` | Perbarui setelah PR P14 merge |

## Bukti teknis yang harus dilampirkan

| Bukti | Cara menghasilkan | Status |
|---|---|---|
| Migrasi berhasil | `001_init.sql`, `seed.sql`, `002_p14.sql`, `verify_p14.sql` lewat `db/run_sql.py` | Lulus, 27 November 2026 |
| Verifikasi skema | `psql "$DATABASE_URL" -f 08_Source/db/verify_p14.sql` | Lulus; ringkasan di `db-verify.txt` |
| 15 test case | `python tests/p14_smoke.py` dengan `SMOKE_EMAIL` dan `SMOKE_PASSWORD` | 15 lulus, 0 gagal, 2 skip |
| Unit test | `pytest` di `08_Source/backend` → 69 lulus, 5 skip | Lulus lokal |
| Lint backend | `ruff check app tests` | Lulus lokal |
| Lint frontend | `npm run lint` | Lulus lokal |
| Build frontend | `npm run build` | Lulus lokal |
| Screenshot alur | Data usaha → asesmen → tinjau → hasil → rencana | 14 gambar desktop + mobile 390 di `screenshots/` |
| Health check staging | `GET /health` | Belum |
| Log dan error bersih | Konsol browser dan log Render | Konsol lokal bersih; log Render belum |

## Hasil eksekusi 27 November 2026

- Project Supabase `growpath`, ref `xckzrccbxxkisrbtrdmx`, region Seoul, PostgreSQL 17.12.
- Migrasi: 160 statement `001_init.sql`, 14 statement seed, 4 statement `002_p14.sql`, 2 statement `verify_p14.sql`.
- Database: 6 dimensi, 31 kriteria (PSY 3, PAS 9), 4 segmen, 31 user, 56 index, view `v_assessment_report`.
- Smoke test: skor 47,92, segmen Branding Enthusiasts, 12 dari 31 kriteria, 3 langkah prioritas.
- Skip: TC-03 (profil sudah ada; 404 sudah diverifikasi pada run pertama) dan TC-07 (butuh akun tanpa profil, verifikasi manual).

## Urutan eksekusi yang disarankan

1. Isi `DATABASE_URL`, jalankan tiga migrasi, lalu `verify_p14.sql`.
2. Jalankan backend dan frontend lokal.
3. Jalankan `tests/p14_smoke.py`; simpan `07_Evidence/P14/smoke-report.json`.
4. Ambil screenshot setiap langkah ke `07_Evidence/P14/screenshots/`.
5. Deploy staging sesuai `P14-Staging-Deployment.md`.
6. Ulangi smoke test ke URL staging.
7. Isi Change Request dari Kartu Kejutan saat kelas.
8. Baru ubah status Gate 2.

## Risiko yang diketahui

- Skor P14 baru 12 dari 31 kriteria; hasil menampilkan cakupan, bukan angka penuh.
- Render Free tidur; demo harus membangunkan backend lebih dulu.
- Supabase gratis tanpa backup harian; jangan pakai data pribadi nyata.
- Diagram deployment P13 belum diperbarui untuk Vercel + Render Free.
