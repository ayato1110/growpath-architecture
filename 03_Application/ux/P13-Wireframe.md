# Wireframe P13 Growpath

**Deliverable:** P13-08
**File sumber:** `P13-Wireframe.figcraft`
**Sumber struktur:** `P13-High-Fidelity.figcraft`

## 1. Tujuan

Wireframe low-fidelity untuk alur utama UMKM. Fokus pada struktur, hierarki, dan satu pertanyaan utama per layar. Tidak memakai warna, gambar, shadow, gradient, atau copy final.

## 2. Layar desktop

| Layar | Pertanyaan | Primary action |
|---|---|---|
| 01 Beranda | Apa yang harus saya lakukan sekarang? | Tombol langkah berikutnya |
| 02 Data usaha | Data apa yang perlu Growpath ketahui? | Simpan dan lanjut |
| 03 Asesmen | Apa kondisi usaha saya saat ini? | Simpan dan lanjut per aspek |
| 04 Tinjau jawaban | Apakah jawaban saya sudah benar? | Hitung skor |
| 05 Hasil | Di mana posisi usaha saya? | Lihat rencana aksi |
| 06 Rencana aksi | Apa langkah berikutnya? | Tandai selesai |
| 07 Konsultasi | Apa yang bisa saya tanyakan? | Kirim pertanyaan |
| 08 Log | Apa yang pernah saya tanyakan? | Buka detail |

## 3. Layar mobile

| Layar | Keterangan |
|---|---|
| M01 Beranda | Langkah berikutnya, skor, tiga dimensi terendah, aktivitas, bottom nav |
| M02 Asesmen | Satu aspek per layar, pertanyaan bertumpuk, aksi bawah |
| M03 Hasil | Skor, segmen, lima dimensi, tiga prioritas, tombol rencana |

## 4. Alur

```text
Masuk -> Data usaha -> Asesmen (5 aspek) -> Tinjau jawaban -> Hasil
      -> Rencana aksi / Konsultasi / Log -> Beranda
```

- Tiga cabang dari Hasil: Rencana aksi, Konsultasi, Log.
- Konsultasi aktif setelah ada skor.
- Log hanya menampilkan konsultasi milik pengguna.

## 5. State

- Empty Beranda.
- Loading Beranda.
- Error Beranda.
- Error form Data usaha.

## 6. Batas

- Bukan prototipe interaktif.
- Tanpa warna, gambar, shadow, atau gradient.
- Data usaha memakai 10 field demografi non-scoring.
- Wireframe adalah penanda struktur, bukan pengganti high-fidelity.
