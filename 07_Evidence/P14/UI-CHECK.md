# P14 · Cek UI Implementasi vs Prototipe

**Tanggal:** 28 November 2026  
**Acuan:** `APP-DEV/DESIGN.md`, high-fidelity FigCraft, dan screenshot implementasi.  
**Bukti:** `screenshots/` (desktop + mobile 390) dan `screenshots-staging/`.

## Ringkasan

Arah visual sesuai: latar `--ground`, sheet putih, aksen `#087f5b`, IBM Plex Sans, tanpa gradient/shadow, satu aksi utama per layar. Tidak ada elemen AI slop. Penyimpangan yang tersisa bersifat struktural, bukan visual.

## Per layar

| Layar | Prototipe | Implementasi | Status | Catatan |
|---|---|---|---|---|
| Data usaha | Progress, form satu kolom, kelompok identitas/kontak/lokasi/sektor/usia, tombol simpan draft dan lanjut | Progress, form satu kolom, 10 field + deskripsi, tombol “Simpan dan lanjut” | Sebagian | Tidak ada tombol simpan draft terpisah; simpan langsung |
| Asesmen | Satu aspek per layar, progress aspek, bantuan, simpan draft otomatis | Daftar 2 aspek, halaman per aspek, progress 0/12, simpan per aspek | Sebagian | Belum autosave; baru 2 dari 5 aspek |
| Tinjau jawaban | Ringkasan 31 jawaban, tombol ubah per aspek | Ringkasan 12 jawaban, tombol ubah, status belum dijawab | Sebagian | Cakupan mengikuti P14 |
| Hasil | Skor 40px, segmen, lima bar dimensi, tiga prioritas, catatan skor bukan AI | Skor 40px, segmen, dua bar dimensi, tiga prioritas, cakupan 12/31 | Sebagian | Dua dimensi dan catatan cakupan; skor tampil 1 desimal |
| Rencana | 3–5 langkah, alasan, tindakan, waktu, status, jalur progres tiga langkah | 3 langkah, alasan, tindakan, target tanggal, status, tandai selesai | Sebagian | Jalur progres tiga langkah belum ada |
| Konsultasi | Kotak pertanyaan, contoh, jawaban dalam sheet, sumber, penafian, log otomatis | Form pertanyaan, jawaban, sumber, penafian, log otomatis | Sesuai arah | Dibangun di P15 |
| Log | Filter tanggal/aspek, tabel desktop, kartu mobile | Daftar kartu, status, waktu, umpan balik | Sebagian | Filter tanggal/aspek belum ada |
| Shell desktop | Sidebar 228px, top bar 48px, sheet inset | Sidebar 228px, top bar, konten max 1120px | Sesuai | - |
| Shell mobile | Bottom nav 4 item berikon | Top bar + nav horizontal 5 item | Tidak sesuai | Perlu bottom nav di P15 |
| Tipografi dan warna | Token DESIGN | Token yang sama, tidak ada warna hardcode baru | Sesuai | - |
| Target sentuh | Minimal 44px di mobile | Tombol dan label form 44px | Sesuai | - |
| Fokus keyboard | Terlihat | `:focus-visible` 2px accent | Sesuai | - |
| Empty/loading/error | Wajib | Ada empty state, `loading.tsx`, `error.tsx`, error field | Sesuai | - |

## Penyimpangan yang perlu ditutup

| Prioritas | Penyimpangan | Rencana |
|---:|---|---|
| P1 | Bottom nav mobile belum ada | Tambah 4 item berikon di P15 |
| P1 | Autosave asesmen belum ada | Simpan per perubahan atau debounce di P15 |
| P2 | Jalur progres tiga langkah di Beranda/Rencana | Tambah komponen progres di P15 |
| P2 | Filter log tanggal dan aspek | Tambah filter di P15 |
| P3 | Skor hasil 1 desimal | Tampilkan 2 desimal bila ruang cukup |
| P3 | Tombol simpan draft profil | Tambah bila alur draft dipakai |

## Kesimpulan

Implementasi **layak dipakai untuk Gate 2**: alur utama jelas, visual konsisten, dan state dasar ada. Belum bisa disebut identik dengan prototipe karena bottom nav, autosave, jalur progres, dan filter log belum dikerjakan.
