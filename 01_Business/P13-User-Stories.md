# USER STORY DAN ACCEPTANCE CRITERIA GROWPATH

**Deliverable:** P13-07
**Pemilik:** Mhd Farras Delvioza
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** v1.0, 8 user story

## 1. Cara membaca

Setiap user story memakai format "Sebagai, saya ingin, supaya" dan acceptance criteria dalam bentuk Given, When, Then. Prioritas mengikuti MoSCoW di `../00_Vision/P13-MoSCoW-Backlog.md`. Semua cerita hanya untuk peran UMKM karena Admin B2G belum masuk MVP.

## 2. US-01 Data usaha

**Prioritas:** Must M-01
**Estimasi:** M
**Rujukan:** UC-02, tabel `umkm_profile`

Sebagai pemilik UMKM, saya ingin mengisi data usaha saya sekali, supaya asesmen dan jawaban AI memakai konteks usaha yang benar.

Acceptance criteria:

1. Given pengguna baru sudah masuk, when membuka aplikasi, then diarahkan ke Data usaha bila profil belum lengkap.
2. Given form data usaha terbuka, when pengguna mengosongkan field wajib lalu menekan lanjut, then field yang salah ditandai teks dan fokus pindah ke field pertama yang salah.
3. Given pengguna mengisi email atau nomor WhatsApp tidak valid, when menyimpan, then sistem menolak dengan pesan spesifik dan isian lain tidak hilang.
4. Given semua field wajib valid, when pengguna menyimpan, then data tersimpan dan bisa dibuka lagi setelah keluar dan masuk.
5. Given data demografi berubah, when asesmen sudah pernah dinilai, then skor tidak berubah.

## 3. US-02 Asesmen per aspek

**Prioritas:** Must M-03
**Estimasi:** L
**Rujukan:** UC-03, tabel `assessment`, `assessment_answer`

Sebagai pemilik UMKM, saya ingin mengisi asesmen satu aspek pada satu waktu, supaya 31 pertanyaan tidak terasa berat.

Acceptance criteria:

1. Given profil lengkap, when pengguna membuka Asesmen, then sistem menampilkan aspek pertama dengan jumlah pertanyaan dan progress lima aspek.
2. Given aspek berisi pertanyaan dengan tipe pilihan tunggal, multi pilih, angka, atau ya atau tidak, when pengguna menjawab, then kontrol input sesuai tipe dan menyimpan pilihan dengan benar.
3. Given pengguna menutup aplikasi di tengah aspek, when membuka lagi, then jawaban yang sudah tersimpan muncul kembali.
4. Given ada pertanyaan wajib yang kosong, when pengguna menekan lanjut, then sistem menahan perpindahan dan menampilkan daftar pertanyaan yang kurang.
5. Given penyimpanan gagal, when pengguna melihat form, then jawaban tetap ada dan status gagal tampil dengan tombol coba lagi.

## 4. US-03 Tinjau dan submit

**Prioritas:** Must M-03
**Estimasi:** M
**Rujukan:** UC-04, layar Tinjau jawaban

Sebagai pemilik UMKM, saya ingin memeriksa jawaban sebelum dihitung, supaya saya tidak mendapat skor dari jawaban yang salah isi.

Acceptance criteria:

1. Given lima aspek selesai, when pengguna membuka Tinjau jawaban, then setiap aspek menampilkan pertanyaan, jawaban terpilih, dan tombol Ubah.
2. Given pengguna menekan Ubah pada satu aspek, when aspek terbuka, then jawaban sebelumnya tetap terisi dan bisa diubah.
3. Given masih ada jawaban wajib kosong, when pengguna melihat halaman tinjau, then tombol Hitung skor nonaktif dan kekurangan disebut.
4. Given semua jawaban lengkap, when pengguna menekan Hitung skor, then jawaban dikunci, skor dihitung, dan pengguna diarahkan ke Hasil.
5. Given perhitungan gagal, when pengguna kembali ke halaman, then status error tampil dan jawaban tidak hilang.

## 5. US-04 Skor dan segmen

**Prioritas:** Must M-03
**Estimasi:** M
**Rujukan:** UC-05, tabel `dimension_score`, `segment`

Sebagai pemilik UMKM, saya ingin melihat posisi usaha saya, supaya saya tahu aspek mana yang perlu dibenahi.

Acceptance criteria:

1. Given asesmen sudah dinilai, when pengguna membuka Hasil, then skor total 0 sampai 100 tampil sebagai angka besar.
2. Given skor total tersedia, when halaman dimuat, then nama segmen dan satu kalimat penjelasan tampil.
3. Given lima aspek dinilai, when pengguna melihat bagian dimensi, then lima bar horizontal tampil dengan nilai masing-masing.
4. Given skor dimensi tersedia, when halaman dimuat, then tiga area prioritas diambil dari skor terendah dengan aturan yang sama setiap kali.
5. Given pengguna mengulang asesmen dengan jawaban identik, when skor dihitung, then hasilnya sama persis.

## 6. US-05 Rencana aksi

**Prioritas:** Must M-03
**Estimasi:** L
**Rujukan:** UC-06, tabel `roadmap`, `milestone`, `progress_log`

Sebagai pemilik UMKM, saya ingin mendapat langkah yang bisa dikerjakan, supaya hasil asesmen tidak berhenti sebagai angka.

Acceptance criteria:

1. Given asesmen sudah dinilai, when pengguna membuka Rencana aksi, then tampil 3 sampai 5 langkah berurutan.
2. Given satu langkah tampil, when pengguna membacanya, then ada alasan, tindakan, dan estimasi waktu.
3. Given pengguna menandai satu langkah selesai, when aksi berhasil, then status berubah dan tercatat di riwayat progres.
4. Given pengguna menandai selesai, when halaman dimuat ulang, then status tetap selesai.
5. Given penyimpanan gagal, when pengguna menandai selesai, then status kembali ke sebelumnya dan pesan gagal tampil.

## 7. US-06 Konsultasi AI

**Prioritas:** Must M-02
**Estimasi:** L
**Rujukan:** UC-07, `../03_Application/ai/P13-AI-Architecture.md`

Sebagai pemilik UMKM, saya ingin bertanya tentang usaha saya, supaya saya mendapat penjelasan yang memakai hasil asesmen saya sendiri.

Acceptance criteria:

1. Given pengguna belum punya skor, when membuka Konsultasi, then sistem menjelaskan bahwa asesmen harus diselesaikan lebih dulu dan menautkan ke Asesmen.
2. Given pengguna sudah punya skor, when mengirim pertanyaan, then jawaban tampil dengan ringkasan, alasan, langkah, sumber bila ada, dan penafian.
3. Given pertanyaan di luar konteks usaha, when model menjawab, then sistem menampilkan penolakan sopan dan mencatat status blocked.
4. Given kuota harian habis, when pengguna mengirim pertanyaan, then pertanyaan tetap tersimpan, pesan menyebut kapan kuota pulih, dan tidak ada jawaban palsu.
5. Given model gagal atau melewati batas waktu, when pengguna menunggu, then status gagal tampil dengan tombol coba lagi dan tidak ada jawaban setengah jadi yang disimpan sebagai sukses.

## 8. US-07 Log dan umpan balik

**Prioritas:** Must M-04
**Estimasi:** M
**Rujukan:** UC-08, tabel `consultation`, `ai_answer_log`

Sebagai pemilik UMKM, saya ingin membaca ulang pertanyaan dan jawaban saya, supaya saya bisa memakai saran yang sama tanpa bertanya dua kali.

Acceptance criteria:

1. Given pengguna pernah bertanya, when membuka Log, then daftar pertanyaan tampil urut terbaru.
2. Given daftar log tampil, when pengguna memfilter tanggal atau aspek, then hanya baris yang sesuai tampil.
3. Given pengguna membuka detail, when halaman dimuat, then pertanyaan, jawaban, sumber, waktu, versi prompt, dan status tampil.
4. Given pengguna menilai jawaban, when memilih Membantu atau Tidak membantu, then pilihan tersimpan dan tetap terlihat setelah halaman dimuat ulang.
5. Given belum ada log, when pengguna membuka Log, then empty state tampil dengan tautan ke Konsultasi.
6. Given pengguna lain punya log, when pengguna membuka daftar, then log pengguna lain tidak pernah tampil.

## 9. US-08 Dashboard

**Prioritas:** Must M-05
**Estimasi:** M
**Rujukan:** UC-09, endpoint `GET /me/dashboard`

Sebagai pemilik UMKM, saya ingin tahu satu hal yang harus saya lakukan sekarang, supaya saya tidak menebak dari banyak angka.

Acceptance criteria:

1. Given pengguna sudah punya asesmen, when membuka Beranda, then satu langkah berikutnya tampil sebagai blok terbesar dengan satu tombol aksi.
2. Given skor dan segmen tersedia, when Beranda dimuat, then keduanya tampil sebagai angka, bukan empat kartu KPI.
3. Given lima dimensi punya skor, when Beranda dimuat, then tiga dimensi terendah tampil sebagai bar horizontal.
4. Given belum ada asesmen, when pengguna membuka Beranda, then empty state menjelaskan manfaat asesmen dan menyediakan tombol Mulai asesmen.
5. Given data gagal dimuat, when pengguna membuka Beranda, then pesan error dan tombol coba lagi tampil tanpa angka palsu.

## 10. Pemetaan ke tes

| User story | Tes black-box minimum |
|---|---|
| US-01 | Daftar, isi data valid, simpan, buka lagi; isi email salah |
| US-02 | Isi dua aspek, tutup, buka lagi, lanjutkan |
| US-03 | Submit dengan satu jawaban kosong, lalu lengkapi |
| US-04 | Ulang asesmen dengan jawaban identik, bandingkan skor |
| US-05 | Tandai satu langkah selesai, muat ulang |
| US-06 | Satu pertanyaan valid, satu di luar konteks, satu saat kuota habis |
| US-07 | Filter log, buka detail, beri umpan balik |
| US-08 | Beranda dengan data, tanpa data, dan saat gagal memuat |

Jumlah minimum 15 tes black-box diturunkan dari tabel ini pada P14.
