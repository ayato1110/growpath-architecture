# DEFINITION OF DONE GROWPATH

**Deliverable:** P13-03
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Sesi arsitektur P13, 22 November 2026
**Status:** v1.0

## 1. Prinsip

Selesai berarti ada bukti yang bisa diperiksa orang lain, bukan pernyataan bahwa pekerjaan sudah dikerjakan. Satu deliverable satu artefak, satu artefak satu pemilik, dan setiap klaim punya tautan.

## 2. DoD tingkat tim

Sebuah pekerjaan dianggap selesai jika seluruh butir berikut terpenuhi:

1. Ada artefak atau kode yang bisa dibuka.
2. Ada bukti uji, screenshot, atau log yang sesuai jenis pekerjaan.
3. Sudah direview minimal satu anggota lain, kecuali pekerjaan pemilik proyek yang direview anggota lain.
4. Dokumentasi yang terdampak sudah diperbarui.
5. Tidak menambah fitur di luar lima Must.
6. Tidak ada rahasia, kunci, atau data pribadi di repo.
7. Keputusan baru tercatat di `../design/DECISIONS.md`.

## 3. DoD per jenis pekerjaan

### 3.1 Kode aplikasi

- Berjalan lokal sesuai README.
- Build produksi berhasil.
- Lint bersih.
- Tes unit untuk logika skor lulus.
- Tes end-to-end untuk alur yang berubah lulus.
- Tidak ada error konsol pada alur utama.
- Layar diuji pada 1440px dan 390px tanpa horizontal scroll.
- Empty, loading, dan error state tersedia.
- Fokus keyboard terlihat dan urutan tab masuk akal.
- Copy mengikuti aturan di `../AGENTS.md`, tanpa label demonstrasi.
- Data layar berasal dari API atau sesi pengguna, bukan dataset desain.

### 3.2 Data dan database

- DDL dapat dijalankan dari database kosong tanpa error.
- Primary key, foreign key, unique, check, dan index yang relevan ada.
- Normalisasi sampai 3NF dibuktikan atau pengecualiannya ditulis.
- Seed data dipisahkan dari data produksi dan diberi header yang jelas.
- Skrip backup dan restore diuji pada salinan, bukan data asli.
- Tidak ada data pribadi nyata di seed.

### 3.3 AI

- Prompt punya versi yang bisa dilacak.
- Setiap panggilan tercatat di `ai_answer_log` dengan model, versi prompt, token, latensi, dan status.
- Guardrail diuji dengan minimal satu pertanyaan di luar konteks.
- Penafian tampil pada setiap jawaban.
- Kuota harian berlaku dan pesan kuota habis menyebut waktu pemulihan.
- AI tidak menghitung skor dan tidak mengarang sumber.
- Data pribadi tidak dikirim ke log tanpa kebutuhan audit.

### 3.4 Dokumen dan diagram

- Ada tujuan, ruang lingkup, dan status.
- Setiap gambar punya nomor, judul, dan sumber atau notasi.
- Diagram bisa diedit, bukan hanya PNG.
- Istilah konsisten dengan `kamus-data-p13.md`.
- Tidak ada angka tanpa sumber atau tanda asumsi.
- Ada bagian "yang belum diverifikasi".

### 3.5 Desain antarmuka

- Satu pertanyaan utama per layar.
- Satu primary action per layar.
- Kontras teks minimal 4.5:1 untuk teks normal.
- Target sentuh minimal 44px.
- Tanpa gradient, glass, glow, shadow diam, sparkle, robot, atau badge AI.
- Mobile 390px punya layout sendiri.
- File desain tersimpan dan tidak diekspor ulang tanpa permintaan pemilik.

## 4. DoD per gate

### Gate 1 Design Review

- Vision v1.0 dibekukan.
- Traceability matrix minimal 5 baris, terpenuhi 14 baris.
- ERD 3NF konsisten dengan use case.
- Backlog MoSCoW dengan Must maksimal lima.
- Repo dan papan kerja aktif, setiap anggota punya kartu atau commit.
- Tim Charter ditandatangani.

### Gate 2 Build Review

- Dua fitur Must berjalan end-to-end dengan database nyata.
- ADR tech stack tertulis dan disetujui.
- Topologi dan deployment diagram final, versi awal ter-deploy ke staging.
- Change Request terdokumentasi dengan keputusan.
- Tidak ada anggota dengan nol kontribusi.

### Gate 3 Dry-run Pitch

- Lima Must berjalan dan ter-deploy.
- UAT dan SUS terlaksana dengan bukti.
- Roadmap dan rencana migrasi tersedia.
- Restore backup terbukti.
- Pitch 7 menit sudah dilatih.

## 5. Yang bukan "selesai"

- Rencana yang belum dieksekusi.
- Mockup yang disebut sebagai fitur jadi.
- Kode yang hanya berjalan di laptop satu orang tanpa README.
- Angka target yang ditulis sebagai hasil.
- Diagram yang dibuat setelah kode untuk membenarkan kode.
- UAT yang belum dijalankan tetapi sudah diklaim.
- Pull request tanpa review.

## 6. Bukti minimum per sprint

| Sprint | Bukti minimum |
|---|---|
| P13 | Vision, MoSCoW, use case, user story, traceability, ERD 3NF, BPMN target, DDL, seed, arsitektur AI, NFR, Gate 1 |
| P14 | Dua fitur live, screenshot desktop dan mobile, tes lulus, staging URL, ADR, Gate 2 |
| P15 | Lima fitur, laporan UAT, skor SUS, bukti restore, roadmap, Gate 3 |
| P16 | Tag v1.0, changelog, pitch 10 slide, akun dan data demo, video cadangan |
