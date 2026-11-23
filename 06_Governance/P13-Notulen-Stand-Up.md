# NOTULEN STAND-UP P13

**Deliverable:** P13-16
**Pemilik:** Moch Haikal Ramadhan
**Tanggal:** 22-23 November 2026
**Fasilitator:** Ripa Bagaskara
**Notulis:** Moch Haikal Ramadhan
**Peserta:** Ripa Bagaskara, Mhd Farras Delvioza, Wisnu Nugroho, Bagas Adinata, Moch Haikal Ramadhan

## 1. Catatan

Notulen ini disusun dari catatan pekerjaan, commit, pull request, dan artefak P13. Ini bukan transkrip verbatim. Tujuannya mencatat keputusan dan tindak lanjut yang bisa diperiksa.

## 2. Agenda

1. Membekukan lingkup MVP dan prioritas Must.
2. Menyamakan use case, BPMN, dan user story.
3. Menyamakan ERD, kamus data, DDL, dan seed.
4. Menetapkan pola aplikasi, struktur folder, dan branch.
5. Menetapkan desain wireframe dan high-fidelity.
6. Menetapkan topologi, NFR, hosting, dan deployment.
7. Menyiapkan Gate 1 dan bukti kontribusi.

## 3. Keputusan

| No | Keputusan | Bukti |
|---:|---|---|
| 1 | MVP memakai lima Must: data usaha, konsultasi AI, rekomendasi, log jawaban AI, dashboard | `00_Vision/P13-MoSCoW-Backlog.md` |
| 2 | Use case final 9 UC, UMKM sebagai aktor utama | `01_Business/use-cases.md` |
| 3 | BPMN target dua proses: asesmen/rekomendasi dan konsultasi/log | `01_Business/bpmn-target.md` |
| 4 | ERD 3NF 23 entitas, termasuk `Consultation` dan `AIAnswerLog` | `02_Data/erd-3nf.md`, `08_Source/db/migrations/001_init.sql` |
| 5 | 31 kriteria scoring, demografi non-scoring, bobot default sama | `02_Data/P13-31-Kriteria.md` |
| 6 | Aplikasi memakai Next.js App Router, FastAPI, Supabase, dan branch `main/dev/feature` | `03_Application/P13-App-Structure.md`, `06_Governance/ADR-002-application-structure.md` |
| 7 | Wireframe dan high-fidelity memakai FigCraft; Tinjau jawaban memuat 31 nilai dan Ubah | `03_Application/ux/` |
| 8 | Hosting awal: Vercel Hobby, Render Free, Supabase Free, Cloudflare Free, Sentry Free, DeepSeek API | `04_Technology/P13-Hosting-Options.md` |
| 9 | Gate 1 Hijau per definisi dosen; konfirmasi mitra menjadi PR14-01 | `06_Governance/P13-Gate-1-Checklist.md` |
| 10 | Tim Charter ditandatangani 23 November 2026 | `06_Governance/P13-Tim-Charter-Signed.pdf` |

## 4. Tindak lanjut

| Aksi | Pemilik | Status |
|---|---|---|
| Tanda tangan Tim Charter | Ripa | Selesai 23 November 2026 |
| Kirim konfirmasi mitra dan simpan balasan | Ripa | Belum, draf siap |
| Catat asumsi 31 kriteria | Ripa dan Wisnu | Selesai, lihat `02_Data/P13-31-Kriteria-Asumsi.md` |
| Pastikan kartu kerja lima anggota | Semua | Selesai, `07_Evidence/P13-WORK-BOARD.md` |
| Review silang use case, ERD, DDL | Ripa, Farras, Wisnu | Selesai, `07_Evidence/P13-CROSS-REVIEW.md` |
| Perbaikan Tinjau jawaban | Farras | Selesai, `03_Application/ux/P13-Tinjau-Fix.md` |
| Bangun fitur P14 | Bagas dan tim | Belum, masuk P14 |
| 15 test case black-box | Farras | Belum, masuk P14 |

## 5. Gate 1

Gate 1 sudah **Hijau** karena seluruh butir Definition of Done terpenuhi:

- Vision v1.0.
- Traceability 15 baris.
- ERD 3NF konsisten.
- MoSCoW maksimal lima Must.
- Repo, work board, dan kontribusi anggota.
- Tim Charter ditandatangani.

Konfirmasi mitra belum ada, tetapi itu **PR14-01**, bukan butir Gate 1.

## 6. Bukti

- `06_Governance/P13-Tim-Charter-Signed.pdf`
- `07_Evidence/P13-WORK-BOARD.md`
- `07_Evidence/P13-CROSS-REVIEW.md`
- `07_Evidence/EVIDENCE-INDEX.md`
- `03_Application/ux/P13-Tinjau-Fix.md`

## 7. Catatan

- Live deployment belum dilakukan; itu pekerjaan P14/P15.
- Konfirmasi mitra tetap wajib sebelum P14.
- Notulen ini bisa dilampirkan sebagai bukti P13-16.
