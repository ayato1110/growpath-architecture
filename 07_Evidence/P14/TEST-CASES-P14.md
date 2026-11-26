# P14 · 15 Test Case Black-Box

**Sumber:** user story P13 dan aturan skor `P13-31-KRITERIA.md`.  
**Lingkup:** data usaha, asesmen Psikografi + Pasar, skor, segmen, rekomendasi.  
**Status:** belum dijalankan. Kolom hasil diisi setelah database nyata tersedia.

## Prasyarat

- `001_init.sql`, `seed.sql`, dan `002_p14.sql` sudah dijalankan.
- Backend dan frontend berjalan.
- Akun `umkm@growpath.id` bisa masuk.

## Test case

| ID | Judul | Prasyarat | Langkah | Hasil yang diharapkan | Status |
|---|---|---|---|---|---|
| TC-01 | Masuk sebagai UMKM | Akun uji ada | Buka `/login`, isi email dan kata sandi UMKM | Diarahkan ke `/app`, nama akun tampil | Belum |
| TC-02 | Peran non-UMKM ditolak | Akun pendamping ada | Masuk, buka `/app/data-usaha` | Halaman menampilkan penolakan atau diarahkan; endpoint data menjawab 403 | Belum |
| TC-03 | Data usaha kosong | Belum pernah mengisi profil | Buka `/app/data-usaha` | Form kosong, tanpa pesan galat, tombol simpan tersedia | Belum |
| TC-04 | Simpan data usaha lengkap | Login UMKM | Isi 10 field, simpan | Data tersimpan, kelengkapan 100%, diarahkan ke asesmen | Belum |
| TC-05 | WhatsApp tidak valid | Login UMKM | Isi WhatsApp `abc`, simpan | Pesan galat pada field WhatsApp, data tidak tersimpan | Belum |
| TC-06 | Sektor tidak valid | Login UMKM | Kirim sektor di luar daftar | Ditolak 422, pesan validasi tampil | Belum |
| TC-07 | Asesmen tanpa profil | Profil dihapus atau akun baru | Buka `/app/asesmen` | Diarahkan ke data usaha, bukan membuat asesmen | Belum |
| TC-08 | Draf asesmen berisi 12 kriteria | Profil lengkap | Buka `/app/asesmen` | Dua aspek: Psikografi 3, Pasar 9 | Belum |
| TC-09 | Simpan jawaban aspek | Draf ada | Jawab 3 kriteria Psikografi, simpan | Jawaban tersimpan, lanjut ke Pasar, progres bertambah | Belum |
| TC-10 | Opsi jawaban tidak dikenal | Draf ada | Kirim `option` yang tidak ada di katalog | Ditolak 422, jawaban lama tidak berubah | Belum |
| TC-11 | Kirim asesmen belum lengkap | Baru 3 dari 12 terjawab | Tekan hitung skor | Ditolak 422, daftar kriteria yang belum dijawab disebut | Belum |
| TC-12 | Skor deterministik | 12 jawaban sama | Kirim dua kali dengan jawaban identik | Skor total dan segmen sama pada kedua hasil | Belum |
| TC-13 | Batas segmen | 12 jawaban dengan skor total 30, 55, 80 | Hitung skor | 30 masuk segmen 2, 55 segmen 3, 80 segmen 4 | Belum |
| TC-14 | Cakupan hasil | Asesmen selesai | Buka `/app/hasil/{id}` | Skor, segmen, dua dimensi, dan teks "12 dari 31 kriteria dinilai" tampil | Belum |
| TC-15 | Rekomendasi dan status | Asesmen selesai | Buka `/app/rencana/{id}`, tandai satu langkah selesai | Tiga langkah dari tiga kriteria terendah; status selesai tersimpan setelah muat ulang | Belum |

## Catatan eksekusi

- Isi kolom status dengan `Lulus` atau `Gagal` dan tautkan tangkapan layar di `07_Evidence/P14/screenshots/`.
- TC-12 memakai jawaban yang sama persis; perbedaan hasil berarti skor tidak deterministik.
- Jangan menulis hasil UAT atau SUS dari test case ini.
