# GATE 1 DESIGN REVIEW GROWPATH

**Deliverable:** Checklist Gate 1
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Tim Growpath P13, 23 November 2026
**Status penilaian:** Hijau, Go

## 1. Ringkasan keputusan

| Butir | Status | Bukti |
|---|---|---|
| Vision v1.0 dibekukan | Terpenuhi | `../00_Vision/P13-Vision-v1.0.md`, status v1.0 tanggal 22 November 2026 |
| Matriks ketelusuran minimal 5 baris | Terpenuhi | `P13-Traceability-Matrix.md`, 15 baris |
| ERD 3NF konsisten dengan use case | Terpenuhi, review silang selesai | `../02_Data/erd-3nf.md`, `../02_Data/diagrams/erd-3nf.drawio`, `../01_Business/use-cases.md`, `../07_Evidence/P13-CROSS-REVIEW.md` |
| Backlog MoSCoW, Must maksimal 5 | Terpenuhi | `../00_Vision/P13-MoSCoW-Backlog.md`, 5 Must |
| Repo dan papan kerja aktif, setiap anggota punya kartu atau commit | Terpenuhi dengan work board repo | `../07_Evidence/P13-WORK-BOARD.md`, repo aktif |
| Tim Charter ditandatangani | Terpenuhi | `P13-Tim-Charter.md`, `P13-Tim-Charter-Signed.pdf` |

**Keputusan:** Hijau. Gate 1 terpenuhi; PR14-01 konfirmasi mitra juga sudah selesai dengan UAT 5 Desember 2026.

## 2. Rincian per butir

### 2.1 Vision v1.0

Terpenuhi. Vision memuat problem, nilai, lingkup, tiga KPI, non-goals, anti-goals, asumsi, dan pernyataan pembekuan. Problem statement ditandai sebagai hipotesis karena belum ada wawancara mitra.

### 2.2 Traceability matrix

Terpenuhi. Lima belas baris menghubungkan kebutuhan ke use case, user story, tabel, layar, endpoint, dan file bukti. Lima Must semuanya tertutup.

### 2.3 ERD 3NF

Terpenuhi dari sisi artefak. ERD memuat 23 entitas, termasuk `Consultation` dan `AIAnswerLog`. Normalisasi 3NF dan pengecualian JSONB dijelaskan di `../02_Data/erd-3nf.md`. Review silang use case, ERD, dan DDL dicatat di `../07_Evidence/P13-CROSS-REVIEW.md`.

### 2.4 MoSCoW

Terpenuhi. Lima Must, empat Should, empat Could, dan daftar Won't fase 2. 31 kriteria dinyatakan sebagai mesin rekomendasi, bukan Must keenam.

### 2.5 Repo dan papan kerja

Terpenuhi dengan work board repo. Repo GitHub aktif dengan branch `main` dan `dev` serta branch protection. Kartu pekerjaan untuk Ripa, Wisnu, Farras, Bagas, dan Haikal ada di `../07_Evidence/P13-WORK-BOARD.md`, masing-masing menautkan artefak atau pull request. GitHub Projects bersifat opsional; work board repo menjadi bukti yang bisa diperiksa.

### 2.6 Tim Charter

Terpenuhi. Charter ditandatangani lima anggota pada 23 November 2026. Bukti: `P13-Tim-Charter-Signed.pdf`.

## 3. Butir P13 di luar Definition of Done Gate 1

| Butir | Status | Catatan |
|---|---|---|
| BPMN target dua proses | Terpenuhi | `../01_Business/bpmn-target.md`, dua proses |
| Use case | Terpenuhi | 9 use case |
| 8 user story dan acceptance criteria | Terpenuhi | `../01_Business/P13-User-Stories.md` |
| Wireframe | Terpenuhi | `../03_Application/ux/` |
| Kamus data | Terpenuhi | `../02_Data/kamus-data-p13.md` |
| DDL dan seed | Terpenuhi | `../08_Source/db/migrations/001_init.sql`, `../08_Source/db/seed/seed.sql` |
| Arsitektur AI dan batasan saran | Terpenuhi | `../03_Application/ai/P13-AI-Architecture.md`, `../03_Application/ai/P13-AI-Guardrails.md` |
| NFR | Terpenuhi | `../04_Technology/P13-NFR.md` |
| Konfirmasi mitra | Selesai | `../07_Evidence/P14-01/README.md`; UAT Sabtu, 5 Desember 2026 pukul 10.00 WIB |
| Bukti kontribusi setiap anggota | Terpenuhi dengan work board | `../07_Evidence/P13-WORK-BOARD.md` |

## 4. Syarat sebelum P14

| Syarat | Status | Bukti |
|---|---|---|
| 1. Tandatangani Tim Charter oleh lima anggota | Terpenuhi | `P13-Tim-Charter-Signed.pdf` |
| 2. Kartu papan kerja setiap anggota dan tautan artefak/PR | Terpenuhi dengan work board repo | `../07_Evidence/P13-WORK-BOARD.md` |
| 3. Konfirmasi mitra dan jadwal UAT | Selesai | `../07_Evidence/P14-01/README.md`; UAT Sabtu, 5 Desember 2026 pukul 10.00 WIB |
| 4. Review silang ERD, DDL, dan use case | Terpenuhi | `../07_Evidence/P13-CROSS-REVIEW.md` |
| 5. Perbaikan temuan Tinjau jawaban | Terpenuhi | `../03_Application/ux/P13-Tinjau-Fix.md` |

Gate 1 sudah **Hijau**: semua butir Definition of Done terpenuhi. Konfirmasi mitra sudah selesai sebagai PR14-01 dengan UAT 5 Desember 2026. Butir 2, 4, dan 5 juga sudah selesai.

## 5. Bahan presentasi 5 menit

| Menit | Isi | Bukti |
|---|---|---|
| 0.00-0.45 | Masalah dan objek Growpath | `../00_Vision/P13-Vision-v1.0.md` |
| 0.45-1.30 | Visi dan tiga KPI | `../00_Vision/P13-Vision-v1.0.md` |
| 1.30-2.15 | BPMN target dua proses | `../01_Business/bpmn-target.md` |
| 2.15-3.00 | ERD 3NF dan alasan entitas konsultasi serta log | `../02_Data/erd-3nf.md` |
| 3.00-3.45 | Use case dan traceability | `P13-Traceability-Matrix.md` |
| 3.45-4.30 | Arsitektur AI dan guardrail | `../03_Application/ai/P13-AI-Architecture.md` |
| 4.30-5.00 | Status dan syarat Gate 1 | dokumen ini |

Presenter ditunjuk dosen di tempat, jadi setiap anggota harus bisa menjelaskan bagian mana pun.

## 6. Risiko yang masih dijaga

- Mitra sudah mengonfirmasi UAT Sabtu, 5 Desember 2026 pukul 10.00 WIB; kirim pengingat H-1.
- Work board harus terus diperbarui agar klaim kontribusi tetap bisa diperiksa.
- Prototipe memakai FigCraft, bukan Figma; perlu konfirmasi dosen bila tuntutan Figma dibaca literal.
- Review silang sudah selesai, tetapi ERD dan DDL harus dicek ulang setiap ada perubahan skema.

Gate 1 tetap **Hijau** karena seluruh butir Definition of Done terpenuhi. Risiko di atas tidak mengubah status Gate 1, tetapi harus ditutup sebelum P14/UAT.
