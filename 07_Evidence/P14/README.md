# P14 · Bukti dan Status

**Tanggal:** 27 November 2026  
**Branch:** `feature/p14-data-usaha-rekomendasi`  
**Lingkup:** dua Must P14, yaitu data usaha dan rekomendasi.

## Status

| Butir Gate 2 | Status | Bukti |
|---|---|---|
| Demo 2 fitur Must end-to-end dengan database nyata | Terbukti lokal + staging | `smoke-report.json`, `smoke-report-staging.json` (15 lulus, 2 skip), `screenshots/`, `screenshots-staging/`; demo kelas belum |
| ADR tech stack tertulis dan disetujui CEO | Lulus | `06_Governance/ADR-001-tech-stack.md`, Accepted 27 November 2026 |
| Topologi dan deployment final, staging | Lulus | Frontend https://growpath-staging.vercel.app, backend https://growpath-api.vercel.app, database Supabase |
| Change Request dari Kartu Kejutan terdokumentasi | Belum | Bergantung skenario kelas |
| Tidak ada anggota dengan nol kontribusi | Lulus | `07_Evidence/P14/CONTRIBUTION-AUDIT.md` |

Jangan mengubah status menjadi selesai tanpa bukti eksekusi dan tangkapan layar.

## Artefak kode

| Artefak | Lokasi |
|---|---|
| Migrasi view laporan | `08_Source/db/migrations/002_p14.sql` |
| Skor deterministik | `08_Source/backend/app/services/scoring.py` |
| Rekomendasi berbasis aturan | `08_Source/backend/app/services/recommendation.py` |
| Endpoint profil, asesmen, rencana | `08_Source/backend/app/api/v1/` |
| UI data usaha, asesmen, hasil, rencana | `08_Source/frontend/app/app/` |
| Tes unit skor dan rekomendasi | `08_Source/backend/tests/test_scoring.py` |
| 15 test case black-box | `07_Evidence/P14/TEST-CASES-P14.md` |
| Skrip smoke test | `08_Source/tests/p14_smoke.py` |
| Verifikasi skema | `08_Source/db/verify_p14.sql` |
| Checklist Gate 2 | `07_Evidence/P14/GATE-2-CHECKLIST.md` |
| Hasil smoke test lokal | `07_Evidence/P14/smoke-report.json` |
| Hasil smoke test staging | `07_Evidence/P14/smoke-report-staging.json` |
| Screenshot staging | `07_Evidence/P14/screenshots-staging/` 5 gambar |
| Verifikasi database | `07_Evidence/P14/db-verify.txt` |
| Screenshot alur | `07_Evidence/P14/screenshots/` 14 gambar desktop + mobile 390 |
| Log eksekusi | `07_Evidence/P14/EXECUTION-LOG.md` |
| Cek UI vs prototipe | `07_Evidence/P14/UI-CHECK.md` |
| Diagram deployment final | `04_Technology/P14-Deployment-Diagram.png` |

## Keputusan yang dipakai

- D-041: dua Must P14.
- D-042: aspek Psikografi dan Pasar.
- D-043: 10 field demografi PRD/DDL, OpenAPI diselaraskan.
- D-044: skor dinormalisasi dari 12 kriteria dan cakupan ditampilkan.
- D-045: rekomendasi berbasis aturan, tanpa AI.
- D-046: SQLAlchemy 2 + psycopg 3, migrasi SQL.

## Belum diklaim

- UAT, SUS, dan hasil pengguna nyata belum dijalankan.
- Skor 31 kriteria penuh belum aktif; P14 baru 12 kriteria.
- Staging belum ter-deploy.
