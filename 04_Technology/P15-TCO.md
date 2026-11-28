# P15 · Estimasi Biaya Infrastruktur 12 Bulan (TCO)

**Tanggal:** 28 November 2026  
**Mata uang:** USD, harga daftar. Kurs asumsi: **Rp16.500/USD**.  
**Sumber harga:** Vercel Pricing, Supabase Pricing, Sentry Pricing, Google Gemini API Pricing. Diakses 28 November 2026.

## 1. Asumsi pemakaian

| Variabel | Nilai |
|---|---:|
| UMKM aktif | 50 |
| Konsultasi AI per bulan | 1.000 |
| Token input per konsultasi | ±2.000 |
| Token output per konsultasi | ±400 |
| Asesmen per bulan | 100 |
| Penyimpanan database | < 500 MB |
| Egress | < 10 GB/bulan |
| Pengguna dashboard | 1–3 |

## 2. Skenario A · Akademik / gratis

| Komponen | Paket | Biaya/bulan | Catatan |
|---|---|---:|---|
| Frontend | Vercel Hobby | $0 | Non-komersial, 1 juta invocation |
| Backend | Vercel Hobby Functions | $0 | 4 jam CPU aktif |
| Database | Supabase Free | $0 | 500 MB, pause setelah 1 minggu idle |
| AI | Gemini 3.5 Flash-Lite free tier | $0 | Konten dipakai Google |
| Monitoring | Sentry Developer | $0 | 1 pengguna, 5 ribu error |
| Domain | Tidak ada / subdomain | $0 | `*.vercel.app` |
| **Total** | | **$0** | |

Risiko: database bisa pause, tidak ada backup harian, deployment bisa terlindungi SSO, dan data free tier AI dipakai untuk peningkatan produk.

## 3. Skenario B · Produksi awal (disarankan)

| Komponen | Paket | Biaya/bulan | Biaya/tahun |
|---|---|---:|---:|
| Frontend + backend | Vercel Pro | $20 | $240 |
| Database | Supabase Pro (Micro) | $25 | $300 |
| AI | Gemini 3.5 Flash-Lite berbayar | ±$1,92 | ±$23 |
| Monitoring | Sentry Team | $26 | $312 |
| Domain | `.id` (estimasi) | ±$1 | ±$12 |
| CDN/WAF | Cloudflare Free | $0 | $0 |
| **Total** | | **±$72,92** | **±$887** |
| **Dengan kontingensi 20%** | | **±$87,50** | **±$1.064** |

Dalam rupiah: sekitar **Rp1,2 juta/bulan** atau **Rp14,4 juta/tahun** sebelum kontingensi; sekitar **Rp17,6 juta/tahun** dengan kontingensi.

Perhitungan AI: 1.000 konsultasi × 2.000 token input = 2 juta token × $0,30/1 juta = $0,60. Output 0,4 juta token × $2,50/1 juta = $1,00. Retry 20% menjadi ±$1,92.

## 4. Skenario C · Tumbuh (100 UMKM, 10.000 konsultasi/bulan)

| Komponen | Paket | Biaya/bulan |
|---|---|---:|
| Vercel Pro + 2 seat | Pro | $60 |
| Supabase Pro + Small compute | Pro | $40 |
| Gemini 3.5 Flash-Lite | Berbayar | ±$19 |
| Sentry Business | Business | $80 |
| Domain + Cloudflare | - | ±$1 |
| **Total** | | **±$200** |

## 5. Yang tidak termasuk

- Biaya pengembangan dan honor tim.
- Biaya UAT dan perjalanan.
- Pajak, PPN, dan biaya transaksi.
- Biaya hukum, akuntansi, dan sertifikasi.
- Biaya desain dan konten.
- Biaya pemulihan bencana di luar backup harian.

## 6. Rekomendasi

1. Gunakan **Skenario A** sampai UAT selesai.
2. Naik ke **Skenario B** sebelum demo institusi: backup harian, proyek tidak pause, dan data AI tidak dipakai Google.
3. Tunda Skenario C sampai ada institusi yang menandatangani lisensi.
4. Aktifkan spend cap di Vercel dan Supabase.
5. Pasang Sentry sebelum UAT agar error pengguna tercatat.

## 7. Sumber

- <https://vercel.com/pricing> — Hobby $0, Pro $20/bulan, Functions dan bandwidth.
- <https://supabase.com/pricing> — Free $0, Pro $25/bulan, backup 7 hari.
- <https://sentry.io/pricing/> — Developer $0, Team $26/bulan, Business $80/bulan.
- <https://ai.google.dev/gemini-api/docs/pricing> — Gemini 3.5 Flash-Lite $0,30 input / $2,50 output per 1 juta token.
