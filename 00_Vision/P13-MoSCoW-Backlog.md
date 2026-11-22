# MOSCOW DAN BACKLOG MVP GROWPATH

**Deliverable:** P13-02
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Sesi arsitektur P13, 22 November 2026
**Status:** v1.0

## 1. Aturan prioritas

1. Fitur Must maksimal lima, sesuai sprint P13-P16.
2. 31 kriteria adalah mesin rekomendasi, bukan fitur Must keenam.
3. Setiap permintaan baru masuk lewat Change Request dengan analisis dampak ke data, aplikasi, teknologi, dan jadwal.
4. Fitur yang tidak masuk Must hanya boleh dikerjakan setelah lima Must berjalan end-to-end.

## 2. Must (lima, tidak boleh lebih)

| ID | Must | Hasil yang dijanjikan | Backlog | Estimasi | Bergantung pada |
|---|---|---|---|---|---|
| M-01 | Data usaha | Profil UMKM tersimpan dan dipakai sebagai konteks asesmen dan konsultasi | B-01 Form data usaha 10 field, simpan draft, validasi email dan WhatsApp | M | Auth |
| M-02 | Konsultasi AI | Pengguna bertanya dan menerima jawaban dengan sumber, penafian, dan batas kuota | B-02 Halaman konsultasi, endpoint konsultasi, prompt v1, guardrail, kuota | L | M-01, M-03 |
| M-03 | Rekomendasi | Skor, segmen, tiga area prioritas, dan 3 sampai 5 langkah aksi | B-03 Mesin skor deterministik, halaman hasil, rencana aksi, tandai selesai | L | M-01 |
| M-04 | Log jawaban AI | Setiap pertanyaan dan jawaban tercatat dan bisa dibuka lagi | B-04 Log otomatis, daftar, filter tanggal dan aspek, detail, umpan balik | M | M-02 |
| M-05 | Dashboard | Satu langkah berikutnya, skor terakhir, progres, aktivitas terakhir | B-05 Ringkasan dashboard, empty state, tautan ke asesmen dan konsultasi | M | M-01, M-03 |

### B-01 Data usaha

Kriteria penerimaan ringkas:

- Sepuluh field demografi tampil dengan label dan bantuan.
- Field wajib tidak bisa kosong saat lanjut.
- Email dan nomor WhatsApp divalidasi di klien dan server.
- Data tersimpan sebagai draft dan bisa dibuka lagi.
- Data demografi tidak mengubah skor.

Rujukan: US-01, `use-cases.md` UC-02, tabel `umkm_profile`.

### B-02 Konsultasi AI

Kriteria penerimaan ringkas:

- Konsultasi hanya bisa dibuka setelah ada skor.
- Pertanyaan dikirim ke backend, bukan langsung ke Gemini.
- Jawaban memuat ringkasan, alasan, langkah, sumber bila ada, dan penafian.
- Setiap jawaban tercatat di `ai_answer_log`.
- Kuota habis menghasilkan pesan yang menyebut waktu pemulihan.

Rujukan: US-06, UC-07, `ai-architecture.md`, endpoint `POST /consultations`.

### B-03 Rekomendasi

Kriteria penerimaan ringkas:

- Skor dihitung dari 31 jawaban, bukan oleh AI.
- Skor total, segmen, dan lima skor dimensi tampil.
- Tiga area prioritas diambil dari skor dimensi terendah dengan aturan yang bisa diuji.
- Rencana aksi berisi 3 sampai 5 langkah dengan alasan, tindakan, dan estimasi waktu.
- Pengguna bisa menandai langkah selesai dan statusnya tersimpan.

Rujukan: US-03, US-04, US-05, UC-04 sampai UC-06, `sql/ddl.sql`.

### B-04 Log jawaban AI

Kriteria penerimaan ringkas:

- Daftar log hanya menampilkan milik pengguna aktif.
- Filter tanggal dan aspek bekerja.
- Detail menampilkan waktu, versi prompt, sumber, dan status.
- Umpan balik "Membantu" atau "Tidak membantu" tersimpan.
- Empty state mengarahkan ke konsultasi.

Rujukan: US-07, UC-08, tabel `ai_answer_log`.

### B-05 Dashboard

Kriteria penerimaan ringkas:

- Satu pertanyaan utama: apa yang harus saya lakukan sekarang.
- Langkah berikutnya adalah blok terbesar.
- Skor dan segmen tampil sebagai angka, bukan empat kartu KPI.
- Progres lima dimensi tampil sebagai bar horizontal.
- Tautan ke asesmen, rencana, konsultasi, dan log berfungsi.
- Empty state muncul bila belum ada asesmen.

Rujukan: US-08, UC-09, endpoint `GET /me/dashboard`.

## 3. Should

| ID | Item | Alasan ditunda | Syarat masuk |
|---|---|---|---|
| S-01 | Riwayat asesmen dan perbandingan skor antar waktu | Butuh data historis yang belum ada | Setelah M-03 stabil |
| S-02 | Ekspor ringkasan hasil ke PDF | Bukan bagian lima Must | Setelah P15 |
| S-03 | Notifikasi email pengingat langkah | Butuh penyedia email dan template | Setelah UAT |
| S-04 | Pencarian pada log jawaban | Volume log MVP masih kecil | Bila log lebih dari 50 baris per pengguna |

## 4. Could

| ID | Item | Catatan |
|---|---|---|
| C-01 | Mode gelap | Tidak masuk MVP, butuh uji kontras ulang |
| C-02 | Bahasa Inggris | Tidak masuk MVP, menambah beban copy |
| C-03 | Panduan penggunaan interaktif | Bisa diganti panduan statis |
| C-04 | Beberapa profil usaha per akun | Melanggar asumsi satu UMKM satu tenant |

## 5. Won't (fase 2)

Mentor marketplace, billing otomatis, WhatsApp API, aplikasi mobile native, white-label, multi-tenant B2G penuh, SAML institusi, RAG penuh, analitik lanjutan, admin CMS lengkap, dashboard B2G, rekomendasi berbasis machine learning.

Alasan: menjaga lima Must selesai dan mencegah scope drift. Item di daftar ini tidak boleh dikerjakan pada P14-P16 tanpa Change Request.

## 6. Urutan pengerjaan

1. Auth dan fondasi.
2. B-01 data usaha.
3. B-03 mesin skor dan hasil.
4. B-05 dashboard versi awal.
5. B-02 konsultasi AI.
6. B-04 log jawaban.
7. B-05 dashboard final dan polish.

Urutan ini mengikuti `IMPLEMENTATION-PLAN.md`, dengan catatan dashboard versi awal dibuat lebih cepat agar vertical slice bisa didemokan.
