# ADR-001 Pilihan Teknologi MVP

- Status: **Accepted**. Disetujui CEO Ripa Bagaskara, 27 November 2026.
- Tanggal: 18 November 2026. Revisi dan persetujuan P14: 27 November 2026.
- Pemilik: Ripa Bagaskara.
- Peninjau: Wisnu Nugroho, Bagas Adinata, Moch Haikal Ramadhan.

## Konteks

Tim perlu membangun MVP lima fitur dalam empat pekan. Teknologi harus cepat dipakai, mudah di-deploy, dan tidak menambah beban operasional. Sejak P13, dua keputusan berubah: model AI awal memakai DeepSeek API, dan hosting awal memakai Vercel Hobby serta Render Free, bukan Railway.

## Keputusan

| Lapisan | Pilihan | Catatan |
|---|---|---|
| Frontend | Next.js 16 App Router, TypeScript, Tailwind CSS 4 | Token warna dari `APP-DEV/DESIGN.md`, server component untuk data |
| Backend | FastAPI, Pydantic v2 | Semua mutasi data lewat backend |
| Akses data | SQLAlchemy 2 dan psycopg 3 | Repository layer, tanpa auto-create tabel |
| Database | Supabase PostgreSQL dan pgvector | DDL di `08_Source/db/migrations`, view laporan di `002_p14.sql` |
| Autentikasi | Supabase Auth; `AUTH_MODE=local` untuk pengembangan | Token HS256 lokal hanya saat `APP_ENV=development` |
| AI | Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`), DeepSeek sebagai cadangan | Tidak dipakai untuk skor atau prioritas (D-050) |
| Hosting | Vercel Hobby (frontend), Render Free (backend), Supabase (database) | Proyek akademik non-komersial; Supabase staging di Seoul; Vercel Pro bila dikomersialkan |

Catatan P14: backend staging memakai Vercel Functions karena Render Free meminta verifikasi kartu kredit (D-049). Render tetap opsi produksi.
| Observability | Sentry | Ditambahkan saat staging |
| Edge dan keamanan | Cloudflare bila waktu memungkinkan | Bukan syarat Gate 2 |

Rujukan keputusan: D-009, D-043 sampai D-046, S2-2B-07, S2-2B-09, S2-2B-10.

## Konsekuensi

- Skor dan rekomendasi deterministik; AI hanya untuk narasi pada P15.
- Tim harus menjaga kontrak API dan skema data.
- Vendor dapat diganti karena akses data dan AI dibungkus lapisan aplikasi.
- Biaya dan kuota AI harus dipantau.
- Render Free tidur setelah tidak dipakai; demo Gate 2 harus membangunkan backend lebih dulu.

## Alternatif yang ditolak

- Membangun seluruh 12 modul dan 49 endpoint pada MVP.
- Dedicated API Gateway pada MVP.
- Multi-tenant B2G penuh pada MVP.
- Railway berbayar sebagai hosting awal.
- Gemini sebagai model utama sebelum kuota dan biaya diuji.
- ORM auto-create tabel sebagai pengganti migrasi SQL.
