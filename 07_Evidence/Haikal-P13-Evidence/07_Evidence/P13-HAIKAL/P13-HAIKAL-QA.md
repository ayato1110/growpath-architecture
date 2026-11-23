# QA Teknologi P13 - Haikal

**Tanggal:** 23 November 2026
**Pemilik:** Moch Haikal Ramadhan
**Scope:** P13-14, P13-15, P13-16, PR14-08, PR14-09

## 1. File yang diperiksa

- `04_Technology/P13-Topology-As-Is.png`
- `04_Technology/P13-Topology-Target.png`
- `04_Technology/P13-Deployment-Diagram.png`
- `04_Technology/P13-Topology-Deployment.drawio`
- `04_Technology/P13-NFR.md`
- `04_Technology/P13-Hosting-Options.md`
- `04_Technology/P13-Security-Checklist.md`
- `08_Source/db/migrations/001_init.sql`
- `08_Source/db/seed/seed.sql`

## 2. Checklist

- [x] Topologi as-is generik: UMKM ke rumah binaan, isi formulir, rekap, konsultasi on-site.
- [x] Topologi target: Vercel Hobby, Render Free, Supabase Free, Cloudflare Free, Sentry Free, DeepSeek API.
- [x] Deployment staging dan production awal terpisah.
- [x] NFR tercatat dan bisa diuji.
- [x] Hosting Opsi 1 dan Opsi 2 tercatat.
- [x] Tidak ada API key atau service role key di frontend.
- [x] Region aplikasi dan data Singapura.
- [x] Backup manual direncanakan untuk Supabase Free.
- [x] DDL dan seed berada di `08_Source/db/`.

## 3. Temuan

- Vercel Hobby hanya untuk non-komersial. Jangan monetisasi selama di Hobby.
- Render Free tidur setelah idle dan butuh sekitar 1 menit untuk bangun.
- Supabase Free pause setelah 1 minggu tanpa aktivitas.
- Supabase Free tidak punya backup otomatis. Backup manual wajib.
- Topologi as-is masih generik; sesuaikan setelah mitra dikonfirmasi.
- Live deployment belum dilakukan.

## 4. Rekomendasi

- Pakai Opsi 1 untuk development P14.
- Naik ke Opsi 2 sebelum UAT: Render Starter + Supabase Pro.
- Deploy live dicatat sebagai pekerjaan P14/P15, bukan P13.
- Jalankan uji NFR di `P13-NFR-Test-Plan.md`.

## 5. Bukti

- `04_Technology/`
- `07_Evidence/EVIDENCE-INDEX.md`
- `07_Evidence/P13-WORK-BOARD.md`
