# DATA CONTOH P13 GROWPATH

**Deliverable:** PR14-05
**Pemilik:** Wisnu Nugroho
**Disusun oleh:** Sesi arsitektur P13, 22 November 2026
**Status:** v1.0, data uji

## 1. Prinsip

Seed adalah data uji, bukan data mitra, bukan data pengguna nyata, dan bukan bukti UAT. Semua nama orang dan usaha bersifat sintetis. Email memakai domain `.invalid` yang tidak dapat dikirimi surat.

File: `../08_Source/db/seed/seed.sql`.

## 2. Jumlah baris

| Tabel | Jumlah | Status aturan 30 baris |
|---|---:|---|
| dimension | 6 | Pengecualian: jumlah aspek ditetapkan framework |
| segment | 4 | Pengecualian: jumlah segmen ditetapkan framework |
| plan | 3 | Pengecualian: paket MVP dan fase 2 sudah tetap |
| criterion | 31 | Terpenuhi, 31 kriteria penuh |
| tenant | 2 | Tenant platform dan tenant uji, bukan mitra |
| user | 30 | Terpenuhi |
| umkm_profile | 30 | Terpenuhi |
| assessment | 30 | Terpenuhi, 29 draft dan 1 submitted |
| assessment_answer | 31 | Satu set lengkap untuk menguji Scoring Service |
| knowledge_document | 1 | Dokumen draft, belum dikurasi |
| knowledge_chunk | 1 | Satu potongan uji, embedding null |

Pengecualian dijelaskan karena `dimension`, `segment`, dan `plan` tidak boleh diisi 30 baris tanpa mengarang data. Menambah baris palsu akan melanggar aturan bukti dan membuat katalog tidak konsisten.

## 3. Isi data

### 3.1 Katalog

- Enam dimensi: Demografi, Psikografi, Proses Internal, Pasar, Lingkungan, Keuangan.
- Lima dimensi dinilai dengan bobot 20 masing-masing. Demografi bobot 0 dan `is_scored = false`.
- 31 kriteria dengan kode PSY-01 sampai KEU-09.
- Setiap kriteria memiliki `scoring_rule` JSONB berisi tipe, opsi, poin, atau bucket numerik.
- Empat segmen dengan ambang 0, 30, 55, 80.
- Tiga paket: Free UMKM, Premium UMKM, B2G Institution. Harga 0 berarti belum ditetapkan, bukan gratis permanen.

### 3.2 Pengguna dan profil

- 30 pengguna dengan nama "Pengguna Uji 01" sampai "Pengguna Uji 30".
- 30 profil dengan nama "Usaha Uji 01" sampai "Usaha Uji 30".
- Sektor berputar antara kuliner, fashion, kriya, perdagangan, dan jasa.
- Gender `undisclosed`, WhatsApp kosong, alamat "Alamat uji nomor n, Kota Uji".

### 3.3 Asesmen

- 30 asesmen draft, satu per profil.
- Asesmen pertama diubah menjadi `submitted` dan diberi 31 jawaban.
- Tidak ada `total_score`, `dimension_score`, atau `segment_id` yang diisi di seed.
- Skor wajib dihitung oleh Scoring Service. Ini mencegah seed menjadi sumber angka yang tidak bisa direproduksi.

Jawaban asesmen uji mengikuti profil yang sama dengan dataset desain: skor rendah di Pasar, Keuangan, dan Lingkungan. Angka hasil tidak ditulis di seed.

### 3.4 Pengetahuan

- Satu dokumen berjudul "Kurikulum UMKM Naik Kelas" dengan status `draft`.
- Satu chunk berisi keterangan katalog, bukan kutipan panjang.
- Embedding null karena belum ada proses embedding pada P13.
- Dokumen ini belum layak dipakai sebagai sumber jawaban produksi sampai dikurasi.

## 4. Cara menjalankan

```bash
psql "$DATABASE_URL" -f ../08_Source/db/migrations/001_init.sql
psql "$DATABASE_URL" -f ../08_Source/db/seed/seed.sql
```

Prasyarat:

- PostgreSQL 15 atau lebih baru.
- Ekstensi `pgcrypto`, `citext`, dan `vector` tersedia. Supabase menyediakan ketiganya.
- Hak membuat tabel dan tipe enum.

## 5. Query pemeriksaan

```sql
-- Jumlah baris
SELECT 'dimension' AS tabel, count(*) FROM dimension
UNION ALL SELECT 'criterion', count(*) FROM criterion
UNION ALL SELECT 'segment', count(*) FROM segment
UNION ALL SELECT 'plan', count(*) FROM plan
UNION ALL SELECT 'user', count(*) FROM "user"
UNION ALL SELECT 'umkm_profile', count(*) FROM umkm_profile
UNION ALL SELECT 'assessment', count(*) FROM assessment
UNION ALL SELECT 'assessment_answer', count(*) FROM assessment_answer;

-- Pastikan belum ada skor yang dikarang
SELECT count(*) AS skor_terisi FROM assessment WHERE total_score IS NOT NULL;

-- Asesmen submitted harus punya 31 jawaban
SELECT a.id, count(aa.id) AS jawaban
FROM assessment a
LEFT JOIN assessment_answer aa ON aa.assessment_id = a.id
WHERE a.status = 'submitted'
GROUP BY a.id;

-- Distribusi tipe input
SELECT input_type, count(*) FROM criterion GROUP BY input_type ORDER BY input_type;

-- Segmen
SELECT code, name, min_score, max_score FROM segment ORDER BY order_no;
```

Hasil yang diharapkan:

- `criterion` 31.
- `user`, `umkm_profile`, dan `assessment` masing-masing 30.
- `skor_terisi` 0.
- Asesmen submitted memiliki 31 jawaban.
- Tipe input mencakup `enum`, `multi_select`, `number`, dan `boolean`.

## 6. Yang tidak boleh dilakukan

- Memakai seed sebagai data mitra pada laporan atau pitch.
- Menyalin nama "Usaha Uji" ke screenshot produk.
- Mengisi skor manual agar terlihat selesai.
- Menambah 30 baris palsu pada tabel referensi hanya untuk memenuhi angka.
- Menganggap dokumen pengetahuan draft sebagai sumber resmi yang sudah dikurasi.

## 7. Hubungan ke DDL

- DDL: `../08_Source/db/migrations/001_init.sql`.
- Kamus data: `kamus-data-p13.md`.
- Aturan skor: `P13-31-Kriteria.md`.
- Seed tidak mengubah aturan skor. Seed hanya menyediakan input.
