# Kepatuhan P13 dan PR14 terhadap Skenario Dosen

**Tanggal:** 23 November 2026
**Sumber:** `Skenario_Project ASP R001.txt` halaman 15, 16, 17, dan 20
**Status:** P13 selesai; PR14 tinggal konfirmasi mitra.

## 1. P13 job per peran

| Peran | Tuntutan dosen | Status | Bukti |
|---|---|---|---|
| CEO / PO | Vision, MoSCoW, DoD, team charter | Selesai | `00_Vision/`, `06_Governance/P13-Definition-of-Done.md`, `P13-Tim-Charter-Signed.pdf` |
| CEO / PO | PR: konfirmasi mitra, BMC | BMC selesai; surat mitra siap kirim | `01_Business/P13-Business-Model-Canvas.md`, `07_Evidence/P14-01/PR14-01-Surat-Konfirmasi-Rumah-Setrika.pdf` |
| Analyst & UI/UX | BPMN 2 proses, use case, 5–8 user story, wireframe | Selesai | `01_Business/`, `03_Application/ux/` |
| Analyst & UI/UX | PR: prototipe hi-fi clickable | Selesai dengan FigCraft | `03_Application/ux/P13-High-Fidelity.figcraft` |
| Database | ERD, kamus data, 3NF | Selesai | `02_Data/erd-3nf.md`, `02_Data/kamus-data-p13.md` |
| Database | PR: DDL, data dummy ≥30 baris | Selesai, diuji Supabase | `08_Source/db/`, `07_Evidence/DDL.png`, `07_Evidence/SEED.png` |
| Programmer | Pola aplikasi, struktur folder, repo/branch | Selesai | `03_Application/P13-App-Structure.md`, `06_Governance/ADR-002-application-structure.md` |
| Programmer | PR: proyek lokal login + role, README | Selesai | `08_Source/`, PR #14 |
| Network / QA | Topologi as-is/to-be, NFR, notulen | Selesai | `04_Technology/P13-Topology-As-Is.png`, `P13-Topology-Target.png`, `P13-NFR.md`, `06_Governance/P13-Notulen-Stand-Up.md` |
| Network / QA | PR: dua opsi hosting, deployment diagram | Selesai tahap awal | `04_Technology/P13-Hosting-Options.md`, `P13-Deployment-Diagram.png` |

## 2. Gate 1

| Butir dosen | Status | Bukti |
|---|---|---|
| Vision v1.0 dibekukan | Terpenuhi | `00_Vision/P13-Vision-v1.0.md` |
| Traceability ≥5 baris | Terpenuhi, 15 baris | `06_Governance/P13-Traceability-Matrix.md` |
| ERD 3NF konsisten dengan use case | Terpenuhi, review silang | `07_Evidence/P13-CROSS-REVIEW.md` |
| MoSCoW, Must maksimal 5 | Terpenuhi | `00_Vision/P13-MoSCoW-Backlog.md` |
| Repo dan papan kerja aktif | Terpenuhi dengan work board repo | `07_Evidence/P13-WORK-BOARD.md` |
| Team charter ditandatangani | Terpenuhi | `06_Governance/P13-Tim-Charter-Signed.pdf` |

**Gate 1: Hijau.** Konfirmasi mitra bukan butir Gate 1; itu PR14-01.

## 3. PR sebelum P14

| Tuntutan halaman 20 | Status | Catatan |
|---|---|---|
| Konfirmasi mitra | Sebagian | Surat Rumah Setrika siap kirim; balasan belum ada |
| Prototipe hi-fi clickable | Selesai | FigCraft, bukan Figma; perlu konfirmasi dosen bila literal Figma |
| DDL | Selesai | `08_Source/db/migrations/001_init.sql` |
| Proyek jalan di lokal: login + role | Selesai | `08_Source/`, PR #14 |
| README cara menjalankan | Selesai | `08_Source/README.md` |
| Dua opsi hosting | Selesai tahap awal | `04_Technology/P13-Hosting-Options.md` |

## 4. Catatan P14

P14 belum dikerjakan:

- Dua fitur Must end-to-end dengan database nyata.
- ADR tech stack final.
- Deploy staging.
- Change Request dari Kartu Kejutan.
- 15 test case black-box.
- TCO 12 bulan.

Live deployment bukan PR14; itu P14/P15.

## 5. Kesimpulan

- **P13:** selesai terhadap definisi dosen; Gate 1 Hijau.
- **PR14:** selesai kecuali balasan konfirmasi mitra; surat Rumah Setrika sudah siap kirim.
- **P14:** belum mulai secara fitur.
- **Risiko kepatuhan:** tool prototipe FigCraft, bukan Figma. Kalau dosen menuntut Figma secara literal, perlu konversi atau persetujuan.
- **Risiko bukti kontribusi:** paket kontribusi P13 Bagas masih berupa ZIP di workspace dan belum diunggah. Work board sudah menyediakan kartu, tetapi bukti unggahan sebaiknya diselesaikan sebelum penilaian.
