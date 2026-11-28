# 04_Technology

Folder ini memuat arsitektur teknologi P13.

## P13

- `P13-NFR.md` - kebutuhan non-fungsional
- `P13-Hosting-Options.md` - dua opsi hosting dan biaya tahap awal
- `P13-Security-Checklist.md` - kontrol keamanan
- `P13-Topology-Deployment.drawio` - topologi as-is, topologi target, dan deployment, tiga halaman
- `P13-Topology-As-Is.png` - alur generik sebelum Growpath
- `P13-Topology-Target.png` - topologi target
- `P13-Deployment-Diagram.png` - deployment

## P14

- `P14-Staging-Deployment.md` - pilihan hosting final, variabel lingkungan, langkah deploy, IP plan, dan rollback.
- `P14-Deployment-Diagram.drawio` dan `.png` - diagram deployment final P14.
- `P15-TCO.md` - estimasi biaya infrastruktur 12 bulan.

Topologi as-is adalah versi generik: UMKM datang ke rumah binaan, mengisi formulir, data direkap lembaga, lalu konsultasi atau pelatihan on-site. Detail lokasi menyesuaikan setelah mitra dikonfirmasi.

Teknologi utama: Cloudflare, Vercel Hobby, Render, Supabase, DeepSeek API, dan Sentry. Region aplikasi di Singapura; database staging Supabase memakai Seoul (ap-northeast-2).
