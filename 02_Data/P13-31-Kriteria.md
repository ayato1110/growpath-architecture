# KATALOG 31 KRITERIA UMKM NAIK KELAS

**Sumber utama:** `REFERENSI/20250425 Kurikulum UMKM Naik Kelas KBUMN.pdf`  
**Bagian:** Profiling Matrix dan Segmenting Matrix  
**Status:** Katalog awal untuk P13, bobot default, perlu finalisasi aturan skor per kriteria  
**Tanggal:** 20 November 2026

## 1. Ringkasan

Materi KBUMN memakai 6 aspek profil. Satu aspek bersifat non-scoring, lima aspek lainnya menghasilkan 31 kriteria penilaian.

| Aspek | Jumlah | Sifat |
|---|---:|---|
| Demografi | 10 field profil | Non-scoring |
| Psikografi | 3 kriteria | Scoring |
| Proses Internal | 4 kriteria | Scoring |
| Pasar | 9 kriteria | Scoring |
| Lingkungan | 6 kriteria | Scoring |
| Keuangan | 9 kriteria | Scoring |
| **Total scoring** | **31** | |

Demografi tidak masuk skor akhir. Demografi hanya menjadi profil usaha.

## 2. Kriteria scoring

### Psikografi

| Kode | Kriteria |
|---|---|
| PSY-01 | Motif Wirausaha |
| PSY-02 | Alasan Memilih Bidang Usaha |
| PSY-03 | Sikap Terhadap Risiko |

### Proses Internal

| Kode | Kriteria |
|---|---|
| INT-01 | Jumlah SDM Bergaji Tetap |
| INT-02 | Sumber Bahan Baku |
| INT-03 | Metode Produksi |
| INT-04 | Pengalaman Pelatihan |

### Pasar

| Kode | Kriteria |
|---|---|
| PAS-01 | Branding |
| PAS-02 | Outlet |
| PAS-03 | Cakupan Pasar |
| PAS-04 | Digitalisasi |
| PAS-05 | Order Sub-kontrak Masuk |
| PAS-06 | Order Sub-kontrak Keluar |
| PAS-07 | Pemahaman Atas Pesaing |
| PAS-08 | Pengalaman Pameran |
| PAS-09 | Pengalaman Penjualan Luar Negeri |

### Lingkungan

| Kode | Kriteria |
|---|---|
| LIN-01 | Legalitas Usaha |
| LIN-02 | Sertifikasi Usaha |
| LIN-03 | Dokumen Perpajakan |
| LIN-04 | Pengalaman Organisasi Usaha |
| LIN-05 | Pengelolaan Sampah dan Limbah |
| LIN-06 | Efisiensi Energi |

### Keuangan

| Kode | Kriteria |
|---|---|
| KEU-01 | Kepemilikan Usaha |
| KEU-02 | Pendanaan Usaha |
| KEU-03 | Rekening Usaha |
| KEU-04 | Pencatatan Transaksi Keuangan |
| KEU-05 | Kepemilikan Laporan Keuangan |
| KEU-06 | Digitalisasi Transaksi Usaha |
| KEU-07 | Pendapatan Usaha Tahunan atau Omzet |
| KEU-08 | Aset Usaha |
| KEU-09 | Laba Bersih Tahunan |

## 3. Field demografi non-scoring

| Kode | Field |
|---|---|
| DEM-01 | Nama Usaha |
| DEM-02 | Nama Lengkap Pemilik |
| DEM-03 | Jenis Kelamin |
| DEM-04 | Usia |
| DEM-05 | Nomor Kontak WhatsApp |
| DEM-06 | Alamat Email |
| DEM-07 | Alamat Domisili |
| DEM-08 | Sektor Usaha |
| DEM-09 | Tahun Berdiri |
| DEM-10 | Lama Usaha |

## 4. Bobot default

Bobot resmi per kriteria tidak ditemukan di teks PDF maupun sumber publik yang diperiksa. PDF hanya menyatakan bahwa terdapat skor dan bobot.

Keputusan sementara:

- Bobot default sama untuk setiap kriteria scoring.
- Bobot disimpan di tabel `Criterion.weight`.
- Total bobot dinormalisasi menjadi 1 atau 100.
- Jika bobot resmi tersedia nanti, cukup ubah data, bukan kode.
- Bobot tidak boleh dihitung oleh AI.

Rumus:

```text
skor_kriteria = nilai ternormalisasi 0..100
total = sum(weight_i * skor_kriteria_i) / sum(weight_i)
```

## 5. Segmen

| Rentang nilai | Segmen | Nama |
|---|---|---|
| 0 sampai kurang dari 30 | Segmen 1 | Foundation Builders |
| 30 sampai kurang dari 55 | Segmen 2 | Branding Enthusiasts |
| 55 sampai kurang dari 80 | Segmen 3 | Commerce Optimizers |
| 80 sampai 100 | Segmen 4 | Sustainability Advocates |

Batas bawah dipakai inklusif. Batas atas eksklusif, kecuali nilai 100 masuk Segmen 4.

## 6. Implikasi data model

Entitas yang dibutuhkan:

- `Dimension` untuk enam aspek.
- `Criterion` untuk 31 kriteria scoring dan 10 field demografi non-scoring.
- `Assessment` untuk satu sesi asesmen.
- `AssessmentAnswer` untuk jawaban per kriteria.
- `DimensionScore` untuk skor per aspek.
- `Segment` untuk empat segmen.
- `Consultation` untuk sesi konsultasi AI.
- `AIAnswerLog` untuk pertanyaan, jawaban, prompt version, guardrail, dan status.

Data dictionary saat ini belum memiliki `Consultation` dan `AIAnswerLog`. Keduanya wajib ditambahkan sebelum fitur konsultasi AI dan log jawaban dibangun.

## 7. Yang masih draft

- Tipe input dan opsi jawaban sudah dibuat sebagai draft di bagian 9.
- Poin per opsi adalah usulan awal, bukan angka resmi KBUMN.
- Bobot resmi per kriteria belum ditemukan. Default sementara sama per kriteria.
- Validasi 31 kriteria dan poin terhadap dokumen resmi KBUMN masih diperlukan.

## 8. Aturan untuk implementasi

- Jangan menaruh 31 kriteria sebagai kode keras di frontend.
- Simpan katalog di database atau satu sumber konfigurasi.
- Tampilkan form per aspek agar pengguna tidak melihat 31 pertanyaan sekaligus.
- Simpan versi katalog agar skor lama tetap dapat direproduksi.
- AI hanya menarasikan hasil dan konteks, bukan menghitung skor.
- Semua jawaban AI harus masuk `AIAnswerLog`.

## 9. Rancangan tipe input dan aturan skor

Legenda tipe:

- **SC** — single choice, pilih satu.
- **MA** — multi-select additive, pilih semua yang sesuai, poin dijumlahkan lalu dibatasi 100.
- **NM** — numeric, dinormalisasi ke 0–100 berdasarkan rentang.
- **BL** — boolean, 0 atau 100.

Semua poin di bawah adalah draft yang dapat diubah melalui konfigurasi.

### 9.1 Psikografi

| Kode | Kriteria | Tipe | Opsi dan poin |
|---|---|---|---|
| PSY-01 | Motif Wirausaha | SC | Kebutuhan bertahan hidup 20; penghasilan tambahan 40; peluang pasar 70; keahlian atau minat 80; membangun usaha berkelanjutan 100 |
| PSY-02 | Alasan Memilih Bidang Usaha | SC | Ikut tren atau kebetulan 20; warisan keluarga 40; pengalaman kerja 60; keahlian atau minat 80; riset pasar dan peluang 100 |
| PSY-03 | Sikap Terhadap Risiko | SC | Menghindari risiko 20; sangat hati-hati 40; seimbang 70; berani dengan perhitungan 100; agresif tanpa perhitungan 30 |

### 9.2 Proses Internal

| Kode | Kriteria | Tipe | Opsi dan poin |
|---|---|---|---|
| INT-01 | Jumlah SDM Bergaji Tetap | NM | 0 orang 0; 1–2 orang 25; 3–5 orang 50; 6–10 orang 75; lebih dari 10 orang 100 |
| INT-02 | Sumber Bahan Baku | SC | Tidak tetap 20; pasar lokal 40; supplier tetap 60; kontrak jangka panjang 80; produksi sendiri dan cadangan 100 |
| INT-03 | Metode Produksi | SC | Manual 20; semi-otomatis 50; otomatis 80; otomatis dengan kendali mutu 100 |
| INT-04 | Pengalaman Pelatihan | MA | Pemasaran 20; keuangan 20; produksi 20; digital 20; manajemen 20 |

### 9.3 Pasar

| Kode | Kriteria | Tipe | Opsi dan poin |
|---|---|---|---|
| PAS-01 | Branding | MA | Logo 25; kemasan 25; media sosial 25; website 25 |
| PAS-02 | Outlet | MA | Toko fisik 25; marketplace 25; reseller 20; distributor 20; gerai sendiri 10 |
| PAS-03 | Cakupan Pasar | SC | Lokal 20; kecamatan atau kota 40; provinsi 60; nasional 80; ekspor 100 |
| PAS-04 | Digitalisasi | MA | Media sosial 20; marketplace 20; website 20; iklan digital 20; pembayaran digital 20 |
| PAS-05 | Order Sub-kontrak Masuk | SC | Tidak pernah 0; pernah sekali 40; beberapa kali 70; rutin atau kontrak 100 |
| PAS-06 | Order Sub-kontrak Keluar | SC | Tidak pernah 0; pernah 40; rutin 70; kontrak 100 |
| PAS-07 | Pemahaman Atas Pesaing | SC | Tidak tahu 0; tahu nama 25; tahu harga dan produk 50; riset berkala 75; analisis strategi 100 |
| PAS-08 | Pengalaman Pameran | SC | Belum 0; lokal 25; regional 50; nasional 75; internasional 100 |
| PAS-09 | Pengalaman Penjualan Luar Negeri | SC | Belum 0; pernah coba 40; rutin ekspor 100 |

### 9.4 Lingkungan

| Kode | Kriteria | Tipe | Opsi dan poin |
|---|---|---|---|
| LIN-01 | Legalitas Usaha | MA | NIB 40; NPWP 30; izin usaha sektoral 30 |
| LIN-02 | Sertifikasi Usaha | MA | Halal 30; BPOM 30; ISO atau SNI 20; HACCP 20 |
| LIN-03 | Dokumen Perpajakan | MA | NPWP 40; status PKP 20; SPT rutin 20; faktur pajak 20 |
| LIN-04 | Pengalaman Organisasi Usaha | SC | Tidak pernah 0; pernah 30; aktif 60; pengurus 100 |
| LIN-05 | Pengelolaan Sampah dan Limbah | MA | Pemilahan 25; bank sampah atau daur ulang 25; pengolahan limbah 25; limbah tersertifikasi 25 |
| LIN-06 | Efisiensi Energi | MA | Lampu LED 20; alat hemat energi 20; energi terbarukan 30; audit energi 30 |

### 9.5 Keuangan

| Kode | Kriteria | Tipe | Opsi dan poin |
|---|---|---|---|
| KEU-01 | Kepemilikan Usaha | SC | Perseorangan 30; CV 50; koperasi 80; PT 100 |
| KEU-02 | Pendanaan Usaha | SC | Pinjaman informal 20; keluarga 30; modal sendiri 40; bank atau koperasi 80; investor 100 |
| KEU-03 | Rekening Usaha | BL | Tidak 0; ya 100 |
| KEU-04 | Pencatatan Transaksi Keuangan | SC | Tidak ada 0; manual sederhana 30; buku atau spreadsheet 60; aplikasi 100 |
| KEU-05 | Kepemilikan Laporan Keuangan | SC | Tidak ada 0; laba rugi 40; laba rugi dan neraca 70; laporan lengkap 100 |
| KEU-06 | Digitalisasi Transaksi Usaha | MA | QRIS 20; transfer bank 20; marketplace 20; POS 20; pembukuan digital 20 |
| KEU-07 | Pendapatan Usaha Tahunan atau Omzet | NM | Lihat bagian 10 |
| KEU-08 | Aset Usaha | NM | Lihat bagian 10 |
| KEU-09 | Laba Bersih Tahunan | NM | Lihat bagian 10 |

### 9.6 Demografi non-scoring

| Kode | Field | Tipe input | Aturan |
|---|---|---|---|
| DEM-01 | Nama Usaha | Text | Wajib |
| DEM-02 | Nama Lengkap Pemilik | Text | Wajib |
| DEM-03 | Jenis Kelamin | Select | Laki-laki, perempuan, atau tidak ingin menyebut |
| DEM-04 | Usia | Number | Tahun, 15–100 |
| DEM-05 | Nomor Kontak WhatsApp | Phone | Format Indonesia |
| DEM-06 | Alamat Email | Email | Validasi email |
| DEM-07 | Alamat Domisili | Text | Wajib |
| DEM-08 | Sektor Usaha | Select | Kuliner, fashion, kriya, pertanian, perdagangan, jasa, teknologi, kesehatan, pendidikan, lainnya |
| DEM-09 | Tahun Berdiri | Year | Empat digit |
| DEM-10 | Lama Usaha | Number | Tahun, minimal 0 |

## 10. Rentang numeric

| Kriteria | Rentang dan skor |
|---|---|
| INT-01 Jumlah SDM | 0 = 0; 1–2 = 25; 3–5 = 50; 6–10 = 75; >10 = 100 |
| KEU-07 Omzet tahunan | <50 juta = 20; 50–300 juta = 40; 300 juta–2,5 miliar = 60; 2,5–10 miliar = 80; >10 miliar = 100 |
| KEU-08 Aset usaha | <50 juta = 20; 50–500 juta = 40; 500 juta–2 miliar = 60; 2–10 miliar = 80; >10 miliar = 100 |
| KEU-09 Laba bersih tahunan | Rugi = 0; 0–50 juta = 30; 50–250 juta = 60; 250 juta–1 miliar = 80; >1 miliar = 100 |

Rentang ini adalah asumsi awal. Jika ada klasifikasi resmi yang berbeda, ubah konfigurasi.

## 11. Aturan skor

### Single choice

Skor kriteria adalah poin opsi yang dipilih.

### Multi-select additive

1. Pengguna memilih semua opsi yang sesuai.
2. Poin setiap opsi dijumlahkan.
3. Hasil dibatasi maksimal 100.
4. Opsi “belum” atau “tidak ada” tidak boleh digabung dengan opsi positif.
5. Jika tidak ada opsi positif yang dipilih, skor 0.

### Numeric

1. Simpan nilai mentah.
2. Petakan nilai ke rentang pada bagian 10.
3. Simpan skor 0–100.
4. Tampilkan nilai mentah dan skor secara terpisah.

### Boolean

Ya = 100, tidak = 0.

### Skor total

```text
skor_total = sum(weight_i * skor_kriteria_i) / sum(weight_i)
```

Default `weight_i = 1/31`.

### Skor dimensi

Skor dimensi adalah rata-rata berbobot dari kriteria di dalam dimensi tersebut.

### Segmen

| Skor total | Segmen |
|---|---|
| 0 sampai kurang dari 30 | Foundation Builders |
| 30 sampai kurang dari 55 | Branding Enthusiasts |
| 55 sampai kurang dari 80 | Commerce Optimizers |
| 80 sampai 100 | Sustainability Advocates |

## 12. Validasi sebelum implementasi

- Cocokkan nama 31 kriteria dengan dokumen KBUMN.
- Validasi opsi jawaban dengan bahasa yang dipakai fasilitator.
- Validasi poin per opsi bersama Ripa dan Wisnu.
- Validasi apakah ada kriteria yang wajib memakai multi-select.
- Uji skor dengan minimal tiga profil UMKM contoh.
- Simpan versi katalog agar skor lama tidak berubah saat opsi diperbarui.
- Jangan menampilkan skor ke pengguna sebelum aturan final disetujui.
