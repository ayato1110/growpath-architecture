# Review Silang Use Case, ERD, dan DDL

**Tanggal:** 23 November 2026
**Reviewer:** Ripa Bagaskara
**Pemilik artefak:** Farras Delvioza (use case), Wisnu Nugroho (ERD/DDL), Ripa Bagaskara (traceability)

## 1. Scope

- 9 use case, UC-01 sampai UC-09.
- 8 user story, US-01 sampai US-08.
- 23 entitas ERD dan 23 tabel DDL.
- 15 endpoint MVP.
- 31 kriteria dan seed data.

## 2. Hasil pemeriksaan

| Pemeriksaan | Hasil | Bukti |
|---|---|---|
| UC-01 sampai UC-09 ada | Lulus, 9 UC | `01_Business/use-cases.md` |
| Semua UC terhubung ke traceability | Lulus | `06_Governance/P13-Traceability-Matrix.md` |
| 8 user story dan acceptance criteria | Lulus | `01_Business/P13-User-Stories.md` |
| ERD dan DDL sama-sama 23 entitas | Lulus | `02_Data/erd-3nf.md`, `08_Source/db/migrations/001_init.sql` |
| `Consultation` dan `AIAnswerLog` ada di ERD dan DDL | Lulus | `02_Data/erd-3nf.md`, `08_Source/db/migrations/001_init.sql` |
| 31 kriteria ada di seed | Lulus | `02_Data/P13-31-Kriteria.md`, `08_Source/db/seed/seed.sql` |
| Skor kosong di seed | Lulus | `07_Evidence/Verifikasi Jumlah Baris & Skor Kosong.png` |
| RLS tenant terpisah | Lulus, 30 vs 0 | `07_Evidence/Uji RLS (Row-Level Security) sebagai Tenant 1 .png`, `Tenant 2` |
| 15 endpoint MVP | Lulus | `03_Application/openapi.yaml` |
| OpenAPI repo | Selesai disinkronkan | `03_Application/openapi.yaml`: 15 path bisnis, 3 endpoint pendukung |

## 3. Temuan

1. Tidak ada konflik struktur antara use case, ERD, dan DDL.
2. `Consultation` dan `AIAnswerLog` konsisten sebagai entitas P13.
3. `assessment_answer` berisi 31 jawaban untuk satu asesmen submitted; 29 asesmen lain masih draft. Ini sesuai `seed-data.md`.
4. OpenAPI repo sebelumnya memuat B2G, admin, mentor, billing, dan notification. Kontrak sudah diselaraskan ke 15 endpoint MVP, ditambah auth dan health sebagai pendukung.
5. Topologi as-is belum tersedia sebagai gambar terpisah; ini bukan bagian ERD/DDL.

## 4. Kesimpulan

Review silang **lulus** untuk use case, ERD, dan DDL. Tidak ada perubahan struktur data yang diperlukan sebelum P14. Sisa pekerjaan adalah sinkronisasi OpenAPI dan topologi as-is, yang dicatat di matrix.
