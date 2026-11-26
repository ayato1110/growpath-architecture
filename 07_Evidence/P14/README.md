# P14 · Bukti dan Status

**Tanggal:** 27 November 2026  
**Branch:** `feature/p14-data-usaha-rekomendasi`  
**Lingkup:** dua Must P14, yaitu data usaha dan rekomendasi.

## Status

| Butir Gate 2 | Status | Bukti |
|---|---|---|
| Demo 2 fitur Must end-to-end dengan database nyata | Belum dijalankan | Menunggu `DATABASE_URL` Supabase |
| ADR tech stack tertulis dan disetujui CEO | Ada, menunggu persetujuan CEO | `06_Governance/ADR-001-tech-stack.md` revisi 27 November 2026 |
| Topologi dan deployment final, staging | Belum | Rencana Vercel Hobby + Render Free + Supabase |
| Change Request dari Kartu Kejutan terdokumentasi | Belum | Bergantung skenario kelas |
| Tidak ada anggota dengan nol kontribusi | Belum diverifikasi | Cek commit dan PR saat penutupan |

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
