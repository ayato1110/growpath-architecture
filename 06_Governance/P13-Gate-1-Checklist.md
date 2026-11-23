# GATE 1 DESIGN REVIEW GROWPATH

**Deliverable:** Checklist Gate 1
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Tim Growpath P13, 23 November 2026
**Status penilaian:** Kuning, Go with conditions

## 1. Ringkasan keputusan

| Butir | Status | Bukti |
|---|---|---|
| Vision v1.0 dibekukan | Terpenuhi | `../00_Vision/P13-Vision-v1.0.md`, status v1.0 tanggal 22 November 2026 |
| Matriks ketelusuran minimal 5 baris | Terpenuhi | `P13-Traceability-Matrix.md`, 15 baris |
| ERD 3NF konsisten dengan use case | Terpenuhi, review silang selesai | `../02_Data/erd-3nf.md`, `../02_Data/diagrams/erd-3nf.drawio`, `../01_Business/use-cases.md`, `../07_Evidence/P13-CROSS-REVIEW.md` |
| Backlog MoSCoW, Must maksimal 5 | Terpenuhi | `../00_Vision/P13-MoSCoW-Backlog.md`, 5 Must |
| Repo dan papan kerja aktif, setiap anggota punya kartu atau commit | Terpenuhi dengan work board repo | `../07_Evidence/P13-WORK-BOARD.md`, repo aktif |
| Tim Charter ditandatangani | Belum | `P13-Tim-Charter.md` bagian tanda tangan masih kosong |

**Keputusan:** Kuning. Boleh lanjut ke P14 dengan syarat di bagian 4.

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

Belum. Isi charter lengkap, tetapi kolom tanda tangan kosong. Ini tidak bisa diklaim selesai sebelum ditandatangani.

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
| Konfirmasi mitra | Sebagian | `../07_Evidence/P13-Partner-Confirmation.md` masih draf |
| Bukti kontribusi setiap anggota | Terpenuhi dengan work board | `../07_Evidence/P13-WORK-BOARD.md` |

## 4. Syarat sebelum P14

| Syarat | Status | Bukti |
|---|---|---|
| 1. Tandatangani Tim Charter oleh lima anggota | Belum | `P13-Tim-Charter.md` |
| 2. Kartu papan kerja setiap anggota dan tautan artefak/PR | Terpenuhi dengan work board repo | `../07_Evidence/P13-WORK-BOARD.md` |
| 3. Konfirmasi mitra dan jadwal UAT | Sebagian, draf | `../07_Evidence/P13-Partner-Confirmation.md` |
| 4. Review silang ERD, DDL, dan use case | Terpenuhi | `../07_Evidence/P13-CROSS-REVIEW.md` |
| 5. Perbaikan temuan Tinjau jawaban | Terpenuhi | `../03_Application/ux/P13-Tinjau-Fix.md` |

Gate 1 tetap **Kuning** karena butir 1 belum ada dan butir 3 baru draf. Butir 2, 4, dan 5 sudah selesai. Konfirmasi mitra tetap wajib sebelum P14; draf boleh dipakai untuk P13.

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

## 6. Risiko bila dipaksakan Hijau

- Kartu papan kerja kosong membuat klaim kontribusi tidak bisa dibuktikan.
- Charter tanpa tanda tangan melemahkan kesepakatan tim.
- Mitra tanpa konfirmasi membuat UAT P15 berisiko ditunda.
- Review silang yang dilewati membuat ERD dan DDL berpotensi tidak sinkron saat implementasi.

Karena itu status Kuning adalah penilaian yang jujur, bukan kekurangan administratif yang disembunyikan.
