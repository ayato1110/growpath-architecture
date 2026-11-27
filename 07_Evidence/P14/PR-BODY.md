# P14 · Data usaha dan rekomendasi end-to-end

## Ringkasan

- Must 1 **data usaha**: form 10 field demografi, validasi backend, simpan ke PostgreSQL.
- Must 3 **rekomendasi**: asesmen Psikografi + Pasar (12 kriteria), skor deterministik, segmen, tiga langkah prioritas berbasis aturan.
- Database Supabase: PK, FK, unique, check, index, dan view `v_assessment_report`.
- OpenAPI diselaraskan: profil memakai 10 field PRD/DDL, `GET /assessments`, submit mengembalikan `ScoreResult`.

## Bukti

- `07_Evidence/P14/smoke-report.json`: 15 lulus, 0 gagal, 2 skip.
- `07_Evidence/P14/db-verify.txt`: PostgreSQL 17.12, 6 dimensi, 31 kriteria, 4 segmen, 56 index, view ada.
- `07_Evidence/P14/screenshots/`: 7 tangkapan layar alur.
- `07_Evidence/P14/EXECUTION-LOG.md`: perintah, hasil, dan bug yang diperbaiki.
- `07_Evidence/P14/TEST-CASES-P14.md`: 15 test case.

Contoh hasil: skor **47,92**, segmen **Branding Enthusiasts**, cakupan **12 dari 31 kriteria**, tiga langkah prioritas.

## Tes

- `pytest`: 69 lulus, 5 skip.
- `ruff check app tests`: bersih.
- `npm run lint`: bersih.
- `npm run build`: berhasil, 13 route.
- SQL: lolos parser PostgreSQL dan dieksekusi di Supabase.

## Yang belum

- Deploy backend Render dan frontend Vercel.
- Demo tatap muka Gate 2.
- TC-07 (akun UMKM tanpa profil) masih verifikasi manual.
- Skor baru 12 dari 31 kriteria; P15 melengkapi.

## Catatan review

- Jangan mengubah skor menjadi perhitungan AI.
- Jangan menambah Must keenam.
- Migrasi `001_init.sql` menghapus tabel; jangan dijalankan di database berisi data tanpa backup.
- Region Supabase staging Seoul (D-048), Vercel/Render Singapura.
