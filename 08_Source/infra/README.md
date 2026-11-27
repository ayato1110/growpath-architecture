# Infra

Folder ini disiapkan untuk konfigurasi deploy dan script operasional. Blueprint staging ada di `../../render.yaml` (Render) dan panduan lengkap di `../../04_Technology/P14-Staging-Deployment.md`.

Struktur final ada di [`../../03_Application/P13-App-Structure.md`](../../03_Application/P13-App-Structure.md).

Aturan utama:

- Rahasia disimpan di dashboard Render, Vercel, dan Supabase, bukan di repo.
- `.env.example` hanya memuat nama variabel.
- Script operasional tidak boleh menulis data produksi tanpa persetujuan.
- Deployment mengikuti `04_Technology/` dan `P13-Hosting-Options.md`.

Implementasi dimulai P14: backend Render Free, frontend Vercel Hobby, database Supabase.
