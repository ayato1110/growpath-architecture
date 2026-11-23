# TOPOLOGI DAN OPSI HOSTING GROWPATH

**Deliverable:** PR14-08, PR14-09
**Pemilik:** Moch Haikal Ramadhan
**Disusun oleh:** Tim Growpath P13, 22 November 2026
**Status:** Draf estimasi. Harga wajib diverifikasi ulang sebelum P14.

## 1. Ringkasan

Dua opsi hosting:

| Opsi | Komposisi | Perkiraan biaya tetap | Kesesuaian |
|---|---|---:|---|
| A, direkomendasikan | Railway Pro, Supabase Pro, Cloudflare Free, Sentry Free | sekitar 55 dolar AS per bulan | Produksi, staging, UAT P15 |
| B, hemat | Railway Hobby, Supabase Free, Cloudflare Free, Sentry Free | sekitar 5 dolar AS per bulan | Prototipe dan demo terbatas |

Biaya AI dihitung terpisah karena bergantung jumlah konsultasi.

Harga diambil dari halaman resmi pada 22 November 2026. Harga dapat berubah. Angka ini estimasi teknis, bukan penawaran.

## 2. Diagram

- Topologi target: `P13-Topology-Target.png`, halaman `Topologi Target` di `P13-Topology-Deployment.drawio`.
- Deployment: `P13-Deployment-Diagram.png`, halaman `Deployment` di file yang sama.
- Notasi: ArchiMate 3.2 Technology Layer, ringkas.

Alur:

```text
Browser
  → Cloudflare (DNS, TLS, rate limit dasar)
  → Railway region Singapura (Next.js, FastAPI)
  → Supabase region Singapura (PostgreSQL, Auth, Storage)
  → Gemini API
  → Sentry
```

## 3. Komponen dan perannya

| Komponen | Peran | Catatan |
|---|---|---|
| Cloudflare | DNS, TLS, cache statis, rate limit dasar | Bukan dedicated API gateway |
| Railway | Menjalankan Next.js dan FastAPI | Satu region, auto deploy dari branch |
| Supabase PostgreSQL | Data utama, pgvector | RLS pada tabel berisiko tinggi |
| Supabase Auth | Email dan kata sandi, JWT | SAML fase 2 |
| Supabase Storage | Dokumen pengetahuan | Belum dipakai pada MVP |
| Gemini API | Model bahasa | Hanya dari backend |
| Sentry | Error frontend dan backend | Paket free, verifikasi kuota |

## 4. Opsi A: Railway Pro dan Supabase Pro

### 4.1 Biaya tetap

| Layanan | Paket | Harga daftar | Catatan |
|---|---|---:|---|
| Railway | Pro | 20 dolar AS per bulan | Termasuk 20 dolar AS usage credit, seat tidak terbatas |
| Railway usage | CPU dan RAM | 20 dolar AS per vCPU per bulan, 10 dolar AS per GB RAM per bulan | Per detik, di luar credit |
| Supabase | Pro | 25 dolar AS per bulan | Termasuk 8 GB disk dan kredit compute Micro 10 dolar AS |
| Supabase compute | Micro | 10 dolar AS per bulan | Tertutup kredit |
| Cloudflare | Free | 0 | Verifikasi fitur rate limit |
| Sentry | Free | 0 | Verifikasi kuota error |

Perkiraan:

- Biaya tetap: 20 + 25 = 45 dolar AS per bulan.
- Usage Railway: dua service kecil, sekitar 0,5 sampai 1 vCPU dan 1 GB RAM efektif. Perkiraan 20 sampai 30 dolar AS per bulan, sebagian tertutup credit.
- Total opsi A: sekitar 50 sampai 65 dolar AS per bulan sebelum biaya AI.
- Untuk anggaran, pakai 55 dolar AS per bulan.

Sumber:

- <https://railway.com/pricing>, diakses 22 November 2026.
- <https://supabase.com/pricing>, diakses 22 November 2026.

### 4.2 Kelebihan

- Supabase Pro menyediakan backup harian 7 hari, penting untuk P15.
- Proyek tidak di-pause karena tidak aktif.
- Railway Pro memberi seat tidak terbatas untuk tim enam orang.
- Sesuai TRD dan topologi Progress 12, region Singapura.

### 4.3 Kekurangan

- Biaya bulanan lebih tinggi.
- Dua vendor dengan tagihan terpisah.
- Belum ada SLA pada paket ini.
- Usage Railway bisa naik bila trafik naik.

## 5. Opsi B: Railway Hobby dan Supabase Free

### 5.1 Biaya tetap

| Layanan | Paket | Harga daftar | Catatan |
|---|---|---:|---|
| Railway | Hobby | 5 dolar AS per bulan | Termasuk 5 dolar AS usage, maksimal 3 anggota per proyek |
| Supabase | Free | 0 | 500 MB database, pause setelah 1 minggu tidak aktif, tanpa backup harian |
| Cloudflare | Free | 0 | Sama |
| Sentry | Free | 0 | Sama |

Perkiraan total: sekitar 5 dolar AS per bulan sebelum biaya AI.

Sumber sama dengan opsi A.

### 5.2 Kelebihan

- Biaya sangat rendah.
- Cukup untuk demo lokal atau staging sementara.
- Tidak perlu kartu kredit untuk mencoba.

### 5.3 Kekurangan

- Supabase Free tidak punya backup harian. Ini blocker untuk UAT dan P15.
- Proyek Free bisa pause setelah satu minggu tidak aktif.
- Database 500 MB cepat penuh bila chunk pengetahuan bertambah.
- Railway Hobby maksimal tiga anggota per proyek, tidak cukup untuk tim enam orang tanpa akun bersama.
- Tidak layak untuk produksi atau demo yang harus selalu hidup.

## 6. Biaya AI

Harga Gemini per 1 juta token, diakses 22 November 2026:

| Model | Input | Output | Catatan |
|---|---:|---:|---|
| Gemini 3.5 Flash-Lite | 0,30 dolar AS | 2,50 dolar AS | Paling hemat |
| Gemini 3.8 Flash | 0,75 dolar AS | 3,75 dolar AS | Sampai 31 Desember 2026 |
| Gemini 3.8 Flash | 1,50 dolar AS | 7,50 dolar AS | Mulai 1 Januari 2027 |

Sumber: <https://ai.google.dev/gemini-api/docs/pricing>, diakses 22 November 2026.

Asumsi satu konsultasi:

- Input 2.500 token: pertanyaan, konteks asesmen, dan maksimal 4 chunk.
- Output 500 token.
- Total 3.000 token per konsultasi.

Biaya per 1.000 konsultasi:

| Model | Input | Output | Total |
|---|---:|---:|---:|
| 3.5 Flash-Lite | 2,5 juta token x 0,30 = 0,75 | 0,5 juta token x 2,50 = 1,25 | 2,00 dolar AS |
| 3.8 Flash, harga 2026 | 2,5 juta x 0,75 = 1,88 | 0,5 juta x 3,75 = 1,88 | 3,76 dolar AS |
| 3.8 Flash, harga 2027 | 2,5 juta x 1,50 = 3,75 | 0,5 juta x 7,50 = 3,75 | 7,50 dolar AS |

Skenario:

| Skenario | Konsultasi per bulan | Flash-Lite | 3.8 Flash 2026 |
|---|---:|---:|---:|
| UAT, 5 pengguna x 30 | 150 | 0,30 dolar AS | 0,56 dolar AS |
| Pilot, 100 pengguna x 30 | 3.000 | 6 dolar AS | 11,28 dolar AS |
| Batas kuota, 100 pengguna x 300 | 30.000 | 60 dolar AS | 112,80 dolar AS |

Model final dipilih di P14. Jangan mengunci model di dokumen ini.

## 7. Total biaya 12 bulan

Asumsi pilot 100 pengguna dengan 30 konsultasi per bulan, model Flash-Lite:

| Komponen | Opsi A | Opsi B |
|---|---:|---:|
| Hosting 12 bulan | 660 dolar AS | 60 dolar AS |
| AI 12 bulan | 72 dolar AS | 72 dolar AS |
| Domain dan email | belum dihitung | belum dihitung |
| **Total** | **sekitar 732 dolar AS** | **sekitar 132 dolar AS** |

Opsi B tidak memenuhi syarat backup dan ketersediaan untuk UAT. Selisih sekitar 600 dolar AS setahun adalah biaya untuk bukti restore, proyek yang tidak pause, dan kolaborasi enam orang.

## 8. Rekomendasi

Pilih opsi A untuk P14 dan P15.

Alasan:

1. Backup harian tersedia, sehingga syarat P15 dapat dipenuhi.
2. Proyek tidak pause, sehingga URL demo tetap hidup.
3. Seat tidak terbatas, sesuai tim enam orang.
4. Sesuai TRD dan topologi yang sudah ada.

Opsi B hanya untuk eksperimen lokal atau staging sementara. Jangan memakai opsi B untuk UAT atau Demo Day.

## 9. Backup dan pemulihan

| Butir | Rencana |
|---|---|
| Backup otomatis | Harian, retensi 7 hari pada Supabase Pro |
| Backup manual sebelum demo | Ekspor `pg_dump` ke storage terpisah |
| Uji restore | P15, pulihkan ke proyek baru, ukur waktu |
| RPO | 24 jam |
| RTO | 4 jam |
| Data uji | Seed terpisah, tidak bercampur data UAT |

## 10. Checklist sebelum deploy

- [ ] Harga diverifikasi ulang pada hari deploy.
- [ ] Region Singapura dipilih untuk Railway dan Supabase.
- [ ] Proyek staging dan produksi terpisah.
- [ ] `.env` tidak masuk repo.
- [ ] Service role key hanya di server.
- [ ] Domain dan TLS aktif.
- [ ] Sentry DSN terpasang.
- [ ] Backup harian aktif.
- [ ] Rate limit Cloudflare dan FastAPI aktif.
- [ ] Health check tersedia.

## 11. Yang belum diverifikasi

- Harga Cloudflare dan Sentry tidak diambil dari halaman resmi pada sesi ini. Keduanya diasumsikan memakai paket Free. Verifikasi saat P14.
- Biaya domain, email transaksional, dan monitoring tambahan belum dihitung.
- Kuota Gemini Free Tier tidak dipakai untuk produksi karena konten dapat dipakai meningkatkan produk.
- Belum ada uji beban yang membuktikan perkiraan usage Railway.
- Pajak dan kurs belum dihitung.
