# ADR-001 Pilihan Teknologi MVP

- Status: Proposed.
- Tanggal: 18 November 2026.
- Pemilik: Ripa Bagaskara.
- Peninjau: Wisnu Nugroho, Bagas Adinata, Moch Haikal Ramadhan.

## Konteks

Tim perlu membangun MVP lima fitur dalam empat pekan. Teknologi harus cepat dipakai, mudah di-deploy, dan tidak menambah beban operasional.

## Keputusan

- Backend memakai FastAPI.
- Database, autentikasi, dan storage memakai Supabase.
- Frontend memakai React atau Next.js.
- Model AI memakai Gemini.
- Deployment awal memakai Railway.
- Edge dan keamanan memakai Cloudflare bila waktu memungkinkan.
- Observability memakai Sentry.

## Konsekuensi

- Tim harus menjaga kontrak API dan skema data.
- Vendor dapat diganti karena akses data dan AI dibungkus lapisan aplikasi.
- Biaya dan kuota AI harus dipantau.

## Alternatif yang ditolak

- Membangun seluruh 12 modul dan 49 endpoint pada MVP.
- Dedicated API Gateway pada MVP.
- Multi-tenant B2G penuh pada MVP.
