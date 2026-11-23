# CATATAN ASUMSI 31 KRITERIA P13

**Deliverable:** P13-22
**Pemilik:** Ripa Bagaskara dan Wisnu Nugroho
**Status:** Asumsi P13, belum divalidasi ke KBUMN
**Tanggal:** 23 November 2026
**Sumber utama:** `02_Data/P13-31-Kriteria.md`, `08_Source/db/seed/seed.sql`

## 1. Tujuan

Dokumen ini mencatat asumsi yang dipakai untuk 31 kriteria agar skor bisa dihitung dan direproduksi. Ini bukan klaim bahwa bobot, opsi, atau poin sudah disetujui KBUMN.

## 2. Asumsi yang dipakai

| No | Asumsi | Dampak |
|---:|---|---|
| A-01 | Enam aspek: Demografi, Psikografi, Proses Internal, Pasar, Lingkungan, Keuangan | Demografi non-scoring; lima aspek lain menghasilkan 31 kriteria |
| A-02 | Bobot default sama, 1 per kriteria | Skor total adalah rata-rata berbobot; belum memakai bobot resmi KBUMN |
| A-03 | Setiap kriteria menghasilkan 0 sampai 100 poin | Skor dimensi dan total memakai skala 0 sampai 100 |
| A-04 | Multi-select memakai cap 100 poin | Pilihan tidak bisa melebihi 100 poin per kriteria |
| A-05 | Numeric memakai bucket rentang | Batas bawah dan atas mengikuti `scoring_rule` di seed |
| A-06 | Enum memakai poin per opsi | Opsi dan poin adalah interpretasi tim |
| A-07 | Segmen memakai batas 0, 30, 55, 80, batas bawah inklusif | Segmen S1 sampai S4 |
| A-08 | 10 field demografi tidak masuk skor | Hanya menjadi konteks profil |
| A-09 | Seed 31 kriteria adalah data uji, bukan data produksi | Skor bisa direproduksi dari seed |
| A-10 | Perubahan poin harus menaikkan versi kriteria dan skor | Skor lama tidak boleh berubah diam-diam |

## 3. Yang belum divalidasi

- Bobot resmi per kriteria dari KBUMN.
- Poin setiap opsi jawaban.
- Batas bucket numerik.
- Apakah semua opsi sudah mencakup kondisi UMKM di lapangan.
- Apakah segmen 0/30/55/80 disetujui institusi.
- Validasi ke mitra atau lembaga pembina.

## 4. Dampak ke skor

- Skor saat ini **deterministik dan dapat direproduksi**, tetapi **provisional**.
- Jangan menyebut skor sebagai standar resmi KBUMN.
- Jika poin berubah:
  1. naikkan `criterion.version` atau `scoring_version`,
  2. perbarui seed,
  3. hitung ulang asesmen yang terdampak,
  4. catat perubahan di `06_Governance/CHANGE-REQUEST-LOG.md`.

## 5. Rencana validasi

1. Bandingkan katalog dengan Profiling Matrix dan Segmenting Matrix KBUMN.
2. Minta review mitra/lembaga pembina untuk opsi dan poin.
3. Catat temuan di `07_Evidence/`.
4. Jika perlu, buat Change Request dan versi kriteria baru.
5. Jalankan ulang tes skor deterministik.

## 6. Bukti

- `02_Data/P13-31-Kriteria.md`
- `08_Source/db/seed/seed.sql`
- `02_Data/seed-data.md`
- `07_Evidence/Verifikasi Jumlah Baris & Skor Kosong.png`

## 7. Batas

Dokumen ini menutup kebutuhan **catatan asumsi**, bukan validasi eksternal. Status P13-22 tetap “Ada dengan asumsi” sampai validasi dilakukan.
