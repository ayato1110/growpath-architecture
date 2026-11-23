# USE CASE GROWPATH

**Deliverable:** P13-06
**Pemilik:** Mhd Farras Delvioza
**Disusun oleh:** Sesi arsitektur P13, 22 November 2026
**Status:** v1.1, perbaikan aktor UC-05 dan UC-09

## 1. Aktor

| Aktor | Jenis | Keterangan |
|---|---|---|
| UMKM | Primer, manusia | Pemilik usaha yang memakai aplikasi |
| Sistem Growpath | Sekunder, sistem | Aktor pendukung. Menghitung skor, menyusun rekomendasi, menyimpan log, menegakkan guardrail. Tidak menginisiasi use case. |
| Layanan AI | Sekunder, sistem eksternal | Aktor pendukung. Model Gemini yang dipanggil hanya dari backend. Tidak menginisiasi use case. |
| Admin Growpath | Primer, manusia | Mengelola katalog dan pengetahuan, tidak masuk UI MVP |

Admin B2G dan pendamping tidak masuk use case MVP karena dashboard B2G belum dibangun.

## 2. Daftar use case

| ID | Use case | Aktor utama | Must | Layar | Endpoint |
|---|---|---|---|---|---|
| UC-01 | Masuk dan daftar | UMKM | Prasyarat | Masuk dan daftar | Supabase Auth |
| UC-02 | Kelola data usaha | UMKM | M-01 | Data usaha, Profil | `GET/PUT/PATCH /me/profile` |
| UC-03 | Isi asesmen per aspek | UMKM | M-03 | Asesmen | `POST /assessments`, `GET /assessments/{id}`, `PUT /assessments/{id}/answers` |
| UC-04 | Tinjau dan submit asesmen | UMKM | M-03 | Tinjau jawaban | `POST /assessments/{id}/submit` |
| UC-05 | Lihat skor dan segmen | UMKM | M-03 | Hasil asesmen | `GET /assessments/{id}/scores` |
| UC-06 | Buka rencana aksi dan tandai langkah | UMKM | M-03 | Rencana aksi | `GET /assessments/{id}/roadmap`, `PATCH /milestones/{id}` |
| UC-07 | Konsultasi AI | UMKM | M-02 | Konsultasi | `POST /consultations` |
| UC-08 | Lihat dan nilai log jawaban | UMKM | M-04 | Log jawaban | `GET /consultations`, `GET /consultations/{id}`, `POST /consultations/{id}/feedback` |
| UC-09 | Pantau dashboard | UMKM | M-05 | Beranda | `GET /me/dashboard` |

Sistem Growpath dan Layanan AI adalah aktor pendukung, bukan aktor utama. Mereka tidak menginisiasi use case. Perannya dijelaskan di catatan diagram dan detail use case.

## 2.1 Diagram use case

File: `diagrams/usecase-mvp.drawio`, PNG `diagrams/usecase-mvp.png`.

Diagram memakai notasi UML 2.5 use case: aktor stick figure, batas sistem, elips use case, asosiasi, dan «include». Isi:

- Aktor UMKM di kiri, terhubung ke sembilan use case, UC-01 sampai UC-09.
- Sistem Growpath adalah aktor pendukung untuk UC-04, UC-05, UC-06, dan UC-09. Tidak digambar sebagai aktor terpisah agar diagram tidak penuh; perannya ada di catatan diagram.
- Layanan AI adalah aktor pendukung untuk UC-07.
- «include» dari UC-04 ke UC-05 dan UC-07 ke UC-08.
- UC-09 tidak meng-include UC-05. Skor di dashboard adalah bagian dari perilaku UC-09, bukan use case terpisah.
- Admin Growpath mengelola katalog di luar UI MVP, jadi tidak digambar.

## 3. Detail use case

### UC-01 Masuk dan daftar

- **Tujuan:** Pengguna mendapat sesi yang sah dan diarahkan ke langkah yang tepat.
- **Prasyarat:** Tidak ada.
- **Pemicu:** Pengguna membuka aplikasi.
- **Alur utama:**
  1. Pengguna membuka halaman masuk.
  2. Pengguna memilih daftar atau masuk.
  3. Sistem memvalidasi email dan kata sandi.
  4. Sistem membuat sesi.
  5. Sistem memeriksa kelengkapan profil.
  6. Bila profil belum lengkap, arahkan ke data usaha; bila lengkap, arahkan ke Beranda.
- **Alur alternatif:** Kredensial salah, tampilkan pesan spesifik tanpa membocorkan apakah email terdaftar. Lupa kata sandi mengirim tautan reset.
- **Pasca kondisi:** Sesi aktif, `tenant_id` diambil dari klaim, bukan dari body.
- **Data:** `user`, `tenant`.

### UC-02 Kelola data usaha

- **Tujuan:** Profil UMKM tersimpan dan lengkap sebagai konteks asesmen dan konsultasi.
- **Prasyarat:** Pengguna sudah masuk.
- **Pemicu:** Profil belum lengkap atau pengguna membuka Data usaha.
- **Alur utama:**
  1. Sistem menampilkan sepuluh field demografi.
  2. Pengguna mengisi field wajib.
  3. Sistem memvalidasi email, nomor WhatsApp, tahun, dan rentang usia.
  4. Pengguna menyimpan draft atau lanjut.
  5. Sistem menyimpan dan menghitung kelengkapan profil.
  6. Bila lengkap, pengguna diarahkan ke asesmen.
- **Alur alternatif:** Field tidak valid ditandai teks di bawah field. Simpan gagal tidak menghapus isian.
- **Pasca kondisi:** `umkm_profile` diperbarui, `completeness_pct` dihitung ulang.
- **Data:** `umkm_profile`, `user`.
- **Catatan:** Data demografi tidak masuk skor berbobot.

### UC-03 Isi asesmen per aspek

- **Tujuan:** Pengguna menjawab 31 kriteria dalam lima aspek tanpa melihat semuanya sekaligus.
- **Prasyarat:** Profil wajib lengkap, pengguna sudah masuk.
- **Pemicu:** Pengguna memilih Asesmen.
- **Alur utama:**
  1. Sistem membuat atau membuka draft asesmen.
  2. Sistem menampilkan aspek pertama, jumlah pertanyaan, dan progress.
  3. Pengguna menjawab pertanyaan sesuai tipe input.
  4. Sistem menyimpan jawaban per pertanyaan dan menampilkan status simpan.
  5. Pengguna lanjut ke aspek berikutnya.
  6. Setelah aspek kelima, sistem mengarahkan ke Tinjau jawaban.
- **Alur alternatif:** Aspek belum lengkap, lanjut ditahan dengan daftar pertanyaan yang kurang. Simpan gagal, jawaban tetap di form dan status gagal ditampilkan.
- **Pasca kondisi:** `assessment` berstatus draft, `assessment_answer` berisi jawaban.
- **Data:** `assessment`, `assessment_answer`, `criterion`, `dimension`.
- **Aturan:** Satu aspek per layar, 31 pertanyaan tidak ditampilkan sekaligus.

### UC-04 Tinjau dan submit asesmen

- **Aktor:** UMKM (utama), Sistem Growpath (pendukung perhitungan).
- **Tujuan:** Pengguna memeriksa jawaban sebelum skor dihitung.
- **Prasyarat:** Semua pertanyaan wajib terjawab.
- **Pemicu:** Pengguna menekan Lanjut dari aspek terakhir.
- **Alur utama:**
  1. Sistem menampilkan ringkasan pertanyaan dan jawaban per aspek.
  2. Pengguna membuka aspek yang ingin diubah.
  3. Pengguna menekan Hitung skor.
  4. Sistem mengunci jawaban dan menandai asesmen submitted.
  5. Sistem menjalankan skor deterministik dan menyimpan hasil.
  6. Sistem menampilkan Hasil asesmen.
- **Alur alternatif:** Jawaban kurang, tombol submit nonaktif dan daftar kekurangan tampil. Perhitungan gagal, status error dengan tombol coba lagi, jawaban tidak hilang.
- **Pasca kondisi:** `assessment` berstatus scored, `dimension_score` terisi, `segment_id` terisi.
- **Data:** `assessment`, `assessment_answer`, `dimension_score`, `segment`.
- **Aturan:** AI tidak terlibat dalam perhitungan.

### UC-05 Lihat skor dan segmen

- **Aktor:** UMKM (utama), Sistem Growpath (pendukung perhitungan dan penyimpanan skor).
- **Tujuan:** Pengguna memahami posisi usaha.
- **Prasyarat:** Asesmen sudah dinilai.
- **Pemicu:** Submit selesai atau pengguna membuka Hasil.
- **Alur utama:**
  1. Sistem menampilkan skor total.
  2. Sistem menampilkan nama segmen dan penjelasan singkat.
  3. Sistem menampilkan lima bar dimensi.
  4. Sistem menampilkan tiga area prioritas.
  5. Sistem menautkan ke Rencana aksi.
- **Alur alternatif:** Skor belum ada, tampilkan empty state dengan tautan ke asesmen.
- **Pasca kondisi:** Tidak ada perubahan data.
- **Data:** `assessment`, `dimension_score`, `segment`.

### UC-06 Buka rencana aksi dan tandai langkah

- **Aktor:** UMKM (utama), Sistem Growpath (pendukung penyusunan rencana dan progres).
- **Tujuan:** Pengguna mendapat langkah berikutnya yang bisa dikerjakan.
- **Prasyarat:** Asesmen sudah dinilai dan roadmap tersedia.
- **Pemicu:** Pengguna membuka Rencana aksi.
- **Alur utama:**
  1. Sistem menampilkan 3 sampai 5 milestone.
  2. Setiap milestone memuat alasan, tindakan, estimasi waktu, dan status.
  3. Pengguna menandai satu langkah selesai.
  4. Sistem menyimpan status dan menulis `progress_log`.
  5. Sistem memperbarui jalur progres tiga langkah.
- **Alur alternatif:** Roadmap belum ada, tampilkan empty state dan tombol buat rencana. Gagal simpan, status dikembalikan dan pesan tampil.
- **Pasca kondisi:** `milestone.status` berubah, `progress_log` bertambah.
- **Data:** `roadmap`, `milestone`, `progress_log`.

### UC-07 Konsultasi AI

- **Aktor:** UMKM (utama), Sistem Growpath (pendukung), Layanan AI (pendukung).
- **Tujuan:** Pengguna mendapat jawaban yang memakai konteks asesmen dan pengetahuan resmi.
- **Prasyarat:** Pengguna sudah masuk dan sudah punya skor.
- **Pemicu:** Pengguna mengirim pertanyaan.
- **Alur utama:**
  1. Sistem memeriksa kuota harian.
  2. Sistem menyusun konteks: profil, skor, segmen, tiga prioritas, potongan pengetahuan.
  3. Sistem mengirim prompt berversimen ke Gemini melalui backend.
  4. Model menghasilkan jawaban.
  5. Sistem menjalankan guardrail.
  6. Sistem menampilkan jawaban, sumber bila ada, dan penafian.
  7. Sistem menyimpan `consultation` dan `ai_answer_log`.
- **Alur alternatif:**
  - Kuota habis: pertanyaan tetap disimpan, pesan menyebut waktu pemulihan.
  - Pertanyaan di luar konteks: jawaban penolakan sopan, dicatat sebagai blocked.
  - Model gagal atau timeout: status failed, pengguna bisa mencoba lagi.
- **Pasca kondisi:** Pertanyaan dan jawaban tercatat, token dan latensi tercatat.
- **Data:** `consultation`, `ai_answer_log`, `knowledge_chunk`, `assessment`.
- **Aturan:** Gemini hanya dipanggil dari backend. Kunci tidak pernah ke browser.

### UC-08 Lihat dan nilai log jawaban

- **Tujuan:** Pengguna bisa membaca ulang pertanyaan dan jawaban.
- **Prasyarat:** Pengguna sudah masuk.
- **Pemicu:** Pengguna membuka Log.
- **Alur utama:**
  1. Sistem menampilkan daftar konsultasi milik pengguna.
  2. Pengguna memfilter berdasarkan tanggal atau aspek.
  3. Pengguna membuka detail.
  4. Sistem menampilkan pertanyaan, jawaban, sumber, waktu, versi prompt, dan status.
  5. Pengguna memberi umpan balik membantu atau tidak membantu.
- **Alur alternatif:** Belum ada log, tampilkan empty state dengan tautan ke konsultasi.
- **Pasca kondisi:** Umpan balik tersimpan di `ai_answer_log`.
- **Data:** `consultation`, `ai_answer_log`.

### UC-09 Pantau dashboard

- **Aktor:** UMKM (utama), Sistem Growpath (pendukung agregasi).
- **Tujuan:** Pengguna tahu apa yang harus dilakukan sekarang.
- **Prasyarat:** Pengguna sudah masuk.
- **Pemicu:** Pengguna membuka Beranda.
- **Alur utama:**
  1. Sistem mengambil asesmen terakhir, skor, segmen, dan milestone aktif.
  2. Sistem memilih satu langkah berikutnya.
  3. Sistem menampilkan skor, segmen, progres lima dimensi, dan aktivitas terakhir.
  4. Pengguna membuka tautan ke asesmen, rencana, konsultasi, atau log.
- **Alur alternatif:** Belum ada asesmen, tampilkan penjelasan singkat dan tombol Mulai asesmen. Gagal memuat, tampilkan pesan dan tombol coba lagi.
- **Pasca kondisi:** Tidak ada perubahan data.
- **Data:** `assessment`, `dimension_score`, `milestone`, `consultation`.

## 4. Hubungan use case ke BPMN

| BPMN | Use case yang dicakup |
|---|---|
| P-01 Asesmen dan Rekomendasi | UC-02, UC-03, UC-04, UC-05, UC-06 |
| P-02 Konsultasi AI dan Log | UC-07, UC-08 |

Detail alur ada di `bpmn-target.md` dan `diagrams/bpmn-target.drawio`.

## 5. Yang belum tercakup

- Admin mengelola katalog kriteria. Masuk P14 dan tidak tampil di UI MVP.
- Pendamping melihat progres UMKM binaan.
- Dashboard B2G.
- Reset kata sandi secara rinci, mengikuti alur Supabase Auth.

Use case di luar daftar ini tidak boleh masuk implementasi tanpa Change Request.
