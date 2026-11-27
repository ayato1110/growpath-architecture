# P14 · Gate 2 Build Review Checklist

**Tanggal:** 27 November 2026  
**Status keseluruhan:** **Belum siap** — menunggu database nyata dan staging.  
**Aturan:** jangan menandai butir lulus tanpa bukti eksekusi.

## Definition of Done dosen

| No | Butir | Status | Bukti yang sudah ada | Kekurangan |
|---:|---|---|---|---|
| 1 | Demo langsung 2 fitur Must end-to-end dengan database nyata | Belum | Kode data usaha, asesmen, skor, segmen, roadmap | `DATABASE_URL` dan eksekusi migrasi |
| 2 | ADR tech stack tertulis dan disetujui CEO | Lulus | `06_Governance/ADR-001-tech-stack.md`, Accepted 27 November 2026 | - |
| 3 | Topologi + deployment diagram final, versi awal ter-deploy ke staging | Sebagian | `04_Technology/P14-Staging-Deployment.md`, `render.yaml` | Deploy ke Render, Vercel, Supabase; perbarui diagram |
| 4 | Change Request dari Kartu Kejutan terdokumentasi dengan keputusan | Belum | `06_Governance/CHANGE-REQUEST-LOG.md` | CR dari skenario kelas belum ada |
| 5 | Tidak ada anggota dengan nol kontribusi | Lulus | `07_Evidence/P14/CONTRIBUTION-AUDIT.md` | Perbarui setelah PR P14 merge |

## Bukti teknis yang harus dilampirkan

| Bukti | Cara menghasilkan | Status |
|---|---|---|
| Migrasi berhasil | `psql "$DATABASE_URL" -f 08_Source/db/migrations/001_init.sql` lalu `seed.sql`, `002_p14.sql` | Belum |
| Verifikasi skema | `psql "$DATABASE_URL" -f 08_Source/db/verify_p14.sql` | Belum |
| 15 test case | `python tests/p14_smoke.py` dengan `SMOKE_EMAIL` dan `SMOKE_PASSWORD` | Belum |
| Unit test | `pytest` di `08_Source/backend` → 69 lulus, 5 skip | Lulus lokal |
| Lint backend | `ruff check app tests` | Lulus lokal |
| Lint frontend | `npm run lint` | Lulus lokal |
| Build frontend | `npm run build` | Lulus lokal |
| Screenshot alur | Data usaha → asesmen → tinjau → hasil → rencana | Belum |
| Health check staging | `GET /health` | Belum |
| Log dan error bersih | Konsol browser dan log Render | Belum |

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
