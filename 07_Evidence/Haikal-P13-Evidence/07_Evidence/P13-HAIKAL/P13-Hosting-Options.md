# HOSTING DAN DEPLOYMENT GROWPATH

**Deliverable:** PR14-08, PR14-09
**Pemilik:** Moch Haikal Ramadhan
**Status:** Final untuk tahap awal P14. Bukan final produksi atau UAT.
**Tanggal:** 23 November 2026

## 1. Keputusan

Tahap awal memakai stack gratis/hemat:

| Komponen | Pilihan awal | Biaya |
|---|---|---:|
| Frontend Next.js | Vercel Hobby | 0 dolar AS |
| Backend FastAPI | Render Free | 0 dolar AS |
| Database, Auth, Storage | Supabase Free | 0 dolar AS |
| DNS dan TLS | Cloudflare Free | 0 dolar AS |
| Error monitoring | Sentry Free | 0 dolar AS |
| Model AI | DeepSeek API `deepseek-flash` | Bayar per token |

Vercel Hobby dipakai karena proyek ini akademik dan non-komersial. Jangan memonetisasi aplikasi selama masih di Hobby. Kalau nanti dikomersialkan, pindah ke Vercel Pro.

## 2. Dua opsi biaya

### Opsi 1: Gratis awal, untuk development P14

| Layanan | Paket | Biaya |
|---|---|---:|
| Vercel frontend | Hobby | 0 |
| Render backend | Free | 0 |
| Supabase | Free | 0 |
| Cloudflare | Free | 0 |
| Sentry | Free | 0 |
| DeepSeek API | Pay as you go | Sekitar 0,0007 dolar AS per konsultasi |

Konsekuensi:

- Vercel Hobby hanya untuk penggunaan personal/non-komersial. Proyek akademik ini memenuhi syarat selama tidak dimonetisasi.
- Vercel Hobby memiliki batas bandwidth, build, dan function invocation.
- Render Free tidur setelah 15 menit tanpa traffic dan butuh sekitar 1 menit untuk bangun.
- Render Free memberi 750 instance hours per workspace per bulan.
- Supabase Free berhenti setelah 1 minggu tanpa aktivitas.
- Supabase Free tidak punya backup harian otomatis. Backup manual wajib.
- Database 500 MB, storage 1 GB, egress 5 GB.
- Cocok untuk development, demo internal, dan uji alur.
- Tidak cocok untuk Demo Day atau UAT tanpa pemanasan dan backup manual.

### Opsi 2: Siap UAT, sebelum P15

| Layanan | Paket | Biaya |
|---|---|---:|
| Vercel frontend | Hobby | 0 |
| Render backend | Starter | 7 dolar AS |
| Supabase | Pro | 25 dolar AS |
| Cloudflare | Free | 0 |
| Sentry | Free | 0 |
| DeepSeek API | Pay as you go | Sekitar 0,0007 dolar AS per konsultasi |

Perkiraan tetap: **32 dolar AS per bulan** sebelum biaya AI.

Kelebihan:

- Render backend tidak tidur.
- Supabase tidak pause.
- Backup harian 7 hari.
- Lebih aman untuk UAT dan demo.
- Vercel Hobby tetap dipakai karena UAT akademik non-komersial. Kalau perlu Vercel Pro, tambah 20 dolar AS per bulan.

## 3. Biaya AI DeepSeek

Harga `deepseek-flash` per 1 juta token:

| Token | Off-peak | Peak |
|---|---:|---:|
| Input cache miss | 0,15 dolar AS | 0,30 dolar AS |
| Output | 0,60 dolar AS | 1,20 dolar AS |

Asumsi satu konsultasi: 2.500 token input dan 500 token output.

| Skenario | Off-peak | Peak |
|---|---:|---:|
| 1 konsultasi | 0,000675 dolar AS | 0,00135 dolar AS |
| 150 konsultasi | 0,10 dolar AS | 0,20 dolar AS |
| 3.000 konsultasi | 2,03 dolar AS | 4,05 dolar AS |
| 30.000 konsultasi | 20,25 dolar AS | 40,50 dolar AS |

Top-up 5 dolar AS cukup untuk sekitar 7.400 konsultasi off-peak. Ini jauh lebih murah daripada paket hosting.

Sumber: <https://api-docs.deepseek.com/quick_start/pricing>, diakses 23 November 2026.

## 4. DeepSeek dari langganan OpenCode?

Tidak bisa dipakai sebagai API aplikasi.

- Langganan OpenCode adalah akses ke coding agent, bukan API key untuk backend Growpath.
- Tidak ada jaminan kuota, format OpenAI-compatible, atau izin untuk dipakai produk.
- Memakai token agent untuk aplikasi berisiko melanggar ketentuan layanan.

Yang benar: buat API key DeepSeek di platform DeepSeek, isi `DEEPSEEK_API_KEY` di backend, dan catat model aktual di `ai_answer_log.model`.

Alternatif tanpa biaya AI: Gemini Free Tier. Namun ketentuan free tier dapat memakai konten untuk peningkatan produk, jadi jangan dipakai untuk data UMKM nyata.

## 5. Topologi

```text
Browser
  -> Cloudflare Free (DNS, TLS)
  -> Vercel Hobby: Next.js
  -> Render Free: FastAPI
  -> Supabase Free: PostgreSQL, Auth, Storage
  -> DeepSeek API
  -> Sentry Free
```

- Frontend berjalan di Vercel Hobby; backend di Render Free.
- Supabase menyimpan data, auth, dan storage.
- DeepSeek hanya dipanggil dari backend.
- Service role key dan `DEEPSEEK_API_KEY` tidak masuk browser.

## 6. Backup

| Butir | Opsi 1 | Opsi 2 |
|---|---|---|
| Backup otomatis | Tidak ada | Harian 7 hari |
| Backup manual | `pg_dump` sebelum demo | `pg_dump` tetap disarankan |
| Restore | Uji di proyek baru | Uji di proyek baru |
| RPO | 24 jam, tergantung backup manual | 24 jam |
| RTO | 4 jam | 4 jam |

## 7. Kapan naik ke Opsi 2

Naik ke Opsi 2 sebelum:

- UAT P15.
- Demo Day.
- Pengguna eksternal memakai aplikasi.
- Data UMKM nyata masuk.
- Backup otomatis dan uptime dibutuhkan.

## 8. Checklist deploy

- [ ] Buat dua proyek Supabase Free: development dan UAT.
- [ ] Buat proyek Vercel Hobby untuk frontend.
- [ ] Buat web service Render untuk backend.
- [ ] Isi env di Vercel/Render, bukan di repo.
- [ ] Set `DEEPSEEK_API_KEY` hanya di backend.
- [ ] Jalankan `08_Source/db/migrations/001_init.sql` dan `08_Source/db/seed/seed.sql`.
- [ ] Aktifkan health check.
- [ ] Jadwalkan `pg_dump` manual.
- [ ] Catat tanggal dan sumber harga.
- [ ] Naik ke Opsi 2 sebelum UAT.

## 9. Sumber

- <https://supabase.com/pricing>, diakses 23 November 2026.
- <https://render.com/docs/free>, diakses 23 November 2026.
- <https://render.com/pricing>, diakses 23 November 2026.
- <https://api-docs.deepseek.com/quick_start/pricing>, diakses 23 November 2026.
- <https://vercel.com/docs/plans/hobby>, diakses 23 November 2026, untuk batas Hobby non-komersial.
