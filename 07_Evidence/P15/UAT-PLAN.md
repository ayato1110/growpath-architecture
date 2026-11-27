# P15 · Rencana UAT

**Tanggal rencana:** Sabtu, 5 Desember 2026, 10.00 WIB  
**Mitra:** Rumah Setrika  
**Status:** belum dijalankan. Dokumen ini rencana, bukan hasil.  
**Ruang lingkup:** dua Must yang sudah berjalan, yaitu data usaha dan rekomendasi (asesmen Psikografi + Pasar, skor, segmen, rencana aksi).

## 1. Tujuan

1. Membuktikan pengguna UMKM dapat mengisi data usaha dan menyelesaikan asesmen tanpa pendampingan teknis.
2. Mengukur pemahaman pengguna terhadap skor, segmen, dan langkah prioritas.
3. Mengumpulkan skor SUS dan catatan perbaikan sebelum P15.

## 2. Peserta dan peran

| Peran | Orang | Tugas |
|---|---|---|
| Fasilitator | Ripa | Membacakan tugas, menjaga waktu, tidak membantu mengisi |
| Pencatat | Farras | Mencatat langkah, kesalahan, kutipan, dan waktu |
| Dukungan teknis | Bagas | Menjaga aplikasi dan jaringan, mencatat error |
| Data dan backup | Wisnu | Memastikan data uji aman dan bisa dipulihkan |
| Dokumentasi | Haikal | Foto, daftar hadir, dan bukti |
| Peserta | 3–5 pelaku UMKM | Mengerjakan tugas secara mandiri |

Minimal tiga peserta. Kalau mitra hanya mengirim satu orang, tambahkan dua pengguna proksi dan tulis statusnya sebagai proksi, bukan pengguna nyata.

## 3. Prasyarat

- Staging aktif, atau aplikasi lokal sebagai cadangan.
- Akun uji siap dan sudah dicoba H-1.
- Data uji tidak memakai data pribadi sensitif.
- Formulir persetujuan dan daftar hadir dicetak.
- Kuesioner SUS dicetak.
- Pengingat H-1 sudah dikirim ke mitra.

## 4. Agenda 90 menit

| Waktu | Kegiatan |
|---|---|
| 10.00–10.10 | Pembukaan, tujuan, persetujuan, dan penjelasan bahwa ini bukan ujian |
| 10.10–10.50 | Tujuh tugas UAT, satu peserta didampingi satu pencatat |
| 10.50–11.00 | Istirahat singkat |
| 11.00–11.10 | Kuesioner SUS |
| 11.10–11.25 | Wawancara singkat: kesulitan, manfaat, saran |
| 11.25–11.30 | Penutup dan foto |

## 5. Skenario berbasis tugas

| ID | Tugas | Langkah | Kriteria berhasil | Target waktu |
|---|---|---|---|---|
| T1 | Mengisi data usaha | Buka Data usaha, isi 10 field, simpan | Data tersimpan, kelengkapan 100%, lanjut ke asesmen | 4 menit |
| T2 | Memahami data yang diminta | Baca label dan bantuan field | Peserta bisa menjelaskan arti empat field tanpa dibantu | 2 menit |
| T3 | Mengisi aspek Psikografi | Jawab 3 pertanyaan, simpan | 3 jawaban tersimpan, pindah ke Pasar | 3 menit |
| T4 | Menyelesaikan aspek Pasar | Jawab 9 pertanyaan, tinjau, hitung skor | Skor dan segmen tampil | 7 menit |
| T5 | Menjelaskan hasil | Baca halaman hasil | Peserta menyebut skor, segmen, dan dua aspek dengan kata sendiri | 3 menit |
| T6 | Membuka dan menandai rencana | Buka rencana, tandai satu langkah selesai, muat ulang | Status selesai bertahan setelah muat ulang | 3 menit |
| T7 | Menangani kesalahan | Isi WhatsApp tidak valid, simpan | Pesan galat muncul dan peserta tahu cara memperbaiki | 2 menit |

## 6. Yang diukur

| Metrik | Cara | Target awal |
|---|---|---|
| Task success rate | Jumlah tugas berhasil dibagi total tugas | ≥ 80% |
| Waktu tugas | Stopwatch per tugas | Rata-rata ≤ 5 menit |
| Error kritis | Jumlah error yang menghentikan tugas | 0 |
| Pemahaman hasil | Peserta menyebut skor dan segmen benar | 4 dari 5 peserta |
| SUS | Kuesioner 10 butir | ≥ 68 (di atas rata-rata) |
| Kutipan | Catatan verbatim | Minimal 5 kutipan |

Angka di atas adalah target, bukan hasil. Jangan menulis skor SUS sebelum kuesioner benar-benar diisi.

## 7. Pembagian alat

- Satu laptop atau tablet per peserta, atau bergiliran dengan pencatat.
- Satu lembar tugas per peserta.
- Satu kuesioner SUS per peserta.
- Satu lembar catatan pencatat.
- Daftar hadir dan formulir persetujuan.
- Koneksi cadangan: tethering.

## 8. Etika dan data

- Minta izin sebelum mengambil foto atau merekam.
- Jangan menampilkan nama, nomor WhatsApp, atau alamat asli di bukti publik.
- Data uji dihapus atau dianonimkan setelah UAT.
- Peserta boleh berhenti kapan saja.

## 9. Risiko

| Risiko | Mitigasi |
|---|---|
| Internet mitra tidak stabil | Siapkan tethering dan aplikasi lokal |
| Peserta tidak terbiasa perangkat | Pendamping hanya membantu perangkat, bukan mengisi |
| Waktu melebihi 90 menit | Prioritaskan T1, T4, T5, T6 |
| Staging belum siap | Jalankan versi lokal, catat statusnya |
| Data mitra sensitif | Gunakan data contoh yang disetujui mitra |

## 10. Output yang harus ada setelah UAT

1. Daftar hadir dan formulir persetujuan.
2. Lembar tugas terisi per peserta.
3. Kuesioner SUS terisi dan skor per peserta.
4. Catatan pencatat dan kutipan.
5. Foto kegiatan yang sudah diizinkan.
6. Laporan UAT singkat: temuan, tingkat keparahan, dan rencana perbaikan.
7. Tautan bukti di `07_Evidence/P15/`.

## 11. Status

Belum dijalankan. Jangan mengisi hasil, skor SUS, atau kutipan sebelum 5 Desember 2026.
