# GATE 1 DESIGN REVIEW GROWPATH

**Deliverable:** Checklist Gate 1
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Sesi arsitektur P13, 22 November 2026
**Status penilaian:** Kuning, Go with conditions

## 1. Ringkasan keputusan

| Butir | Status | Bukti |
|---|---|---|
| Vision v1.0 dibekukan | Terpenuhi | `vision-v1.md`, status v1.0 tanggal 22 November 2026 |
| Matriks ketelusuran minimal 5 baris | Terpenuhi | `traceability-matrix.md`, 15 baris |
| ERD 3NF konsisten dengan use case | Terpenuhi, menunggu review silang | `erd-3nf.md`, `diagrams/erd-3nf.drawio`, `use-cases.md` |
| Backlog MoSCoW, Must maksimal 5 | Terpenuhi | `moscow-backlog.md`, 5 Must |
| Repo dan papan kerja aktif, setiap anggota punya kartu atau commit | Sebagian | Repo aktif, kartu papan kerja belum terlihat |
| Tim Charter ditandatangani | Belum | `tim-charter.md` bagian tanda tangan masih kosong |

**Keputusan:** Kuning. Boleh lanjut ke P14 dengan syarat di bagian 4.

## 2. Rincian per butir

### 2.1 Vision v1.0

Terpenuhi. Vision memuat problem, nilai, lingkup, tiga KPI, non-goals, anti-goals, asumsi, dan pernyataan pembekuan. Problem statement ditandai sebagai hipotesis karena belum ada wawancara mitra.

### 2.2 Traceability matrix

Terpenuhi. Lima belas baris menghubungkan kebutuhan ke use case, user story, tabel, layar, endpoint, dan file bukti. Lima Must semuanya tertutup.

### 2.3 ERD 3NF

Terpenuhi dari sisi artefak. ERD memuat 23 entitas, termasuk `Consultation` dan `AIAnswerLog`. Normalisasi 3NF dan pengecualian JSONB dijelaskan di `erd-3nf.md`. Syarat: Wisnu melakukan review silang terhadap use case dan DDL sebelum P14.

### 2.4 MoSCoW

Terpenuhi. Lima Must, empat Should, empat Could, dan daftar Won't fase 2. 31 kriteria dinyatakan sebagai mesin rekomendasi, bukan Must keenam.

### 2.5 Repo dan papan kerja

Sebagian. Repo GitHub aktif dengan branch `main` dan `dev` serta branch protection. Bukti kartu papan kerja untuk setiap anggota belum ada di folder ini. Yang dibutuhkan:

1. Kartu untuk Ripa, Wisnu, Farras, Bagas, dan Haikal.
2. Setiap kartu menautkan artefak atau pull request.
3. Minimal satu commit atau PR per anggota pada P13.

### 2.6 Tim Charter

Belum. Isi charter lengkap, tetapi kolom tanda tangan kosong. Ini tidak bisa diklaim selesai sebelum ditandatangani.

## 3. Butir P13 di luar Definition of Done Gate 1

| Butir | Status | Catatan |
|---|---|---|
| BPMN target dua proses | Terpenuhi | `bpmn-target.md`, dua proses |
| Use case | Terpenuhi | 9 use case |
| 8 user story dan acceptance criteria | Terpenuhi | `user-stories.md` |
| Wireframe | Tidak dikerjakan session ini | High-fidelity FigCraft sudah ada, wireframe formal tidak dipisahkan |
| Kamus data | Terpenuhi | `kamus-data-p13.md` |
| DDL dan seed | Terpenuhi | `sql/ddl.sql`, `sql/seed.sql` |
| Arsitektur AI dan batasan saran | Terpenuhi | `ai-architecture.md` |
| NFR | Terpenuhi | `nfr.md` |
| Konfirmasi mitra | Belum | `partner-confirmation.md` masih draf |
| Bukti kontribusi setiap anggota | Sebagian | Lihat 2.5 |

## 4. Syarat sebelum P14

1. Tandatangani Tim Charter oleh lima anggota.
2. Buat kartu papan kerja untuk setiap anggota dan tautkan minimal satu artefak atau commit.
3. Kirim surat konfirmasi mitra dan simpan balasannya, atau catat penolakan beserta rencana pengguna proksi.
4. Review silang ERD, DDL, dan use case oleh Database Architect dan Analyst.
5. Perbaiki temuan Tinjau jawaban pada audit desain 22 November sebelum alur itu diimplementasikan.

Butir 1 dan 2 wajib untuk mengubah status Gate 1 menjadi Hijau. Butir 3 dan 4 wajib sebelum P14 dimulai. Butir 5 wajib sebelum fitur Tinjau jawaban masuk P14.

## 5. Bahan presentasi 5 menit

| Menit | Isi | Bukti |
|---|---|---|
| 0.00-0.45 | Masalah dan objek Growpath | `vision-v1.md` |
| 0.45-1.30 | Visi dan tiga KPI | `vision-v1.md` |
| 1.30-2.15 | BPMN target dua proses | `bpmn-target.md` |
| 2.15-3.00 | ERD 3NF dan alasan entitas konsultasi serta log | `erd-3nf.md` |
| 3.00-3.45 | Use case dan traceability | `traceability-matrix.md` |
| 3.45-4.30 | Arsitektur AI dan guardrail | `ai-architecture.md` |
| 4.30-5.00 | Status dan syarat Gate 1 | dokumen ini |

Presenter ditunjuk dosen di tempat, jadi setiap anggota harus bisa menjelaskan bagian mana pun.

## 6. Risiko bila dipaksakan Hijau

- Kartu papan kerja kosong membuat klaim kontribusi tidak bisa dibuktikan.
- Charter tanpa tanda tangan melemahkan kesepakatan tim.
- Mitra tanpa konfirmasi membuat UAT P15 berisiko ditunda.
- Review silang yang dilewati membuat ERD dan DDL berpotensi tidak sinkron saat implementasi.

Karena itu status Kuning adalah penilaian yang jujur, bukan kekurangan administratif yang disembunyikan.
