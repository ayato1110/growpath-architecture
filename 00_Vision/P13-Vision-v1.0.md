# VISION v1.0 GROWPATH

**Deliverable:** P13-01
**Pemilik:** Ripa Bagaskara
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Direview oleh:** menunggu review tim
**Status:** v1.0, dibekukan 22 November 2026 atas persetujuan pemilik proyek

## 1. Pernyataan visi

Menjadi infrastruktur digital pertumbuhan UMKM yang menghubungkan pelaku usaha, pendamping, dan institusi pembinaan.

Growpath adalah perusahaan platform advisory UMKM, bukan proses internal satu UMKM. Produk intinya membantu pemilik usaha mengetahui posisi usahanya, memilih langkah berikutnya, dan memantau progres dengan cara yang konsisten.

## 2. Masalah

Pemilik UMKM sering tidak tahu aspek usaha mana yang perlu dibenahi lebih dulu, langkah apa yang harus diambil setelah asesmen, dan apakah usahanya berkembang setelah menjalankan saran. Panduan yang konsisten biasanya mahal karena bergantung pada konsultan swasta atau kapasitas pendamping yang terbatas.

Program pembinaan masih banyak memakai formulir manual, spreadsheet, dan saran lisan. Akibatnya hasil antar UMKM sulit dibandingkan, riwayat saran tidak tercatat, dan institusi pembina tidak punya bukti dampak yang rapi.

Growpath menjawab masalah itu dengan tiga hal yang saling terikat: profiling 31 kriteria, skor deterministik yang bisa diaudit, dan konsultasi AI yang setiap jawabannya tercatat.

**Status bukti:** problem statement ini berasal dari brief dosen, Progress 12, dan diskusi tim. Belum ada wawancara mitra atau riset lapangan baru pada P13. Karena itu klaim masalah di dokumen ini adalah hipotesis yang harus diuji di UAT P15, bukan temuan lapangan.

## 3. Nilai yang ditawarkan

| Pihak | Nilai |
|---|---|
| UMKM | Tahu posisi usaha, dapat langkah berikutnya yang spesifik, bisa bertanya kapan saja dengan biaya rendah |
| Pendamping | Melihat kondisi dan progres UMKM secara ringkas, tanpa menyalin formulir manual |
| Institusi pembina | Mendapat data agregat dan bukti perubahan, bukan laporan naratif tanpa dasar |
| Growpath | Model lisensi B2G yang tidak membebani UMKM untuk layanan inti |

Pembeda produk bukan label AI. Pembeda ada pada kombinasi framework pembinaan yang dipakai institusi, skor yang konsisten dan bisa direproduksi, serta jejak jawaban AI yang bisa diperiksa.

## 4. Lingkup MVP

### Masuk MVP

1. Data usaha.
2. Konsultasi AI.
3. Rekomendasi.
4. Log jawaban AI.
5. Dashboard UMKM.

31 kriteria adalah mesin rekomendasi, bukan fitur Must keenam. Dashboard B2G belum dibangun.

### Di luar MVP

Mentor marketplace, billing otomatis, WhatsApp API, aplikasi mobile native, white-label, multi-tenant B2G penuh, SAML institusi, RAG penuh, analitik lanjutan, admin CMS lengkap, dan rekomendasi berbasis model machine learning.

## 5. Tiga KPI

Target di bawah adalah target produk, bukan hasil pengukuran. Belum ada data penggunaan pada P13.

| KPI | Definisi | Target | Cara ukur | Status |
|---|---|---:|---|---|
| Penyelesaian asesmen | Persentase asesmen yang dibuka dan berhasil disubmit, dibagi asesmen yang dibuka | 70% | Event `assessment_started` dan `assessment_submitted` di database aplikasi | Belum diukur |
| Waktu asesmen | Median waktu dari asesmen dimulai sampai submit, tanpa menghitung jeda antar sesi lebih dari 30 menit | di bawah 12 menit | Selisih `started_at` dan `submitted_at` setelah pembersihan jeda | Belum diukur |
| Kejelasan langkah berikutnya | Persentase pengguna yang menjawab "jelas" atau "sangat jelas" pada pertanyaan tunggal setelah membaca hasil | 4 dari 5 | Pertanyaan UAT skala 1 sampai 5 | Belum diukur |

Metrik pendukung, bukan KPI:

- 60% pengguna kembali dalam 7 hari.
- Minimal 80% jawaban AI dinilai berguna pada uji terbatas.
- Median waktu jawaban AI di bawah 15 detik.

## 6. Pemangku kepentingan

| Pihak | Kepentingan utama |
|---|---|
| UMKM | Panduan yang jelas, murah, dan tidak menghakimi |
| Institusi pembina | Bukti dampak dan efisiensi pembinaan |
| Pendamping | Alat bantu follow-up, bukan pengganti peran manusia |
| Tim Growpath | Produk yang selesai dalam empat pekan tanpa melewati batas MVP |
| Regulator dan vendor | Kepatuhan data, keamanan, dan biaya yang terkendali |

## 7. Non-goals dan anti-goals

Non-goals MVP sudah disebut di bagian 4.

Anti-goals, hal yang membuat produk dianggap gagal walaupun secara teknis berjalan:

- Skor berubah untuk jawaban yang sama.
- AI dipakai untuk menghitung skor.
- Jawaban AI tidak tercatat atau tidak punya penafian.
- Dashboard menampilkan angka yang tidak bisa dijelaskan asalnya.
- Fitur fase 2 masuk sebelum lima Must selesai.
- Produk hanya nyaman di desktop.

## 8. Asumsi dan risiko

| Asumsi | Dampak bila salah |
|---|---|
| Institusi pembina bersedia membayar lisensi dan UMKM memakai layanan inti gratis | Model B2G tidak jalan, perlu BMC ulang |
| Framework 31 kriteria mewakili kondisi UMKM sasaran | Skor dan rekomendasi kurang relevan |
| Pengguna bersedia menjawab 31 pertanyaan dalam lima aspek | Tingkat penyelesaian turun, perlu asesmen bertahap |
| Satu UMKM cukup terikat pada satu tenant pada MVP | Kasus UMKM multi-institusi tidak terlayani |
| Kuota AI harian cukup untuk kebutuhan konsultasi | Pengguna tertahan atau biaya naik |

Risiko utama: skor belum diverifikasi ke dokumen resmi KBUMN, mitra UAT belum ada, dan kapasitas tim terbatas. Mitigasi ada di `nfr.md`, `partner-confirmation.md`, dan `ai-architecture.md`.

## 9. Pernyataan pembekuan

Vision v1.0 ini dibekukan untuk P14. Perubahan pada visi, objek, lima Must, model B2G, atau prinsip skor deterministik hanya boleh lewat Change Request dan dicatat di `../design/DECISIONS.md`.
