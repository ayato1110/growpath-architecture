# P15 · Status PR15

**Tanggal:** 27 November 2026  
**Arti PR15:** pekerjaan rumah sebelum P15, bukan pull request GitHub.

| Butir PR15 | Status | Bukti atau catatan |
|---|---|---|
| Gap analysis per domain | Ada, draf | `GAP-ANALYSIS.md` |
| Jadwal UAT terkonfirmasi | Ada | Rumah Setrika, 5 Desember 2026, 10.00 WIB |
| Skenario UAT berbasis tugas | Ada | `UAT-PLAN.md`, tujuh tugas |
| Kuesioner SUS 10 butir | Ada | `SUS-KUESIONER.md` |
| Backup dan restore | Selesai (logis) | `backup_restore.py` diuji: backup semua tabel, restore ke schema terpisah, 0 selisih di `BACKUP-SCRIPT.txt`; `pg_dump` tidak dipakai |
| Transaksi proses kritis | Ada | Submit asesmen memakai satu commit; perlu tes rollback |
| Konsultasi AI dan log jawaban | Ada, teruji lokal + staging | `services/ai.py`, `/consultations`, UI konsultasi dan log; Gemini 3.5 Flash-Lite; bukti `AI-PROBE-LOCAL.json`, `AI-PROBE-STAGING.json`, `screenshots-staging/` |
| Dokumentasi route/endpoint | Sebagian | OpenAPI diperbarui; daftar route per role belum |
| TCO 12 bulan | Ada | `04_Technology/P15-TCO.md` |
| Staging | Selesai | https://growpath-staging.vercel.app dan https://growpath-api.vercel.app |
| MVP hampir lengkap | Sebagian | 4 dari 5 Must ada; dashboard belum |

## Bukti AI

- `AI-PROBE-LOCAL.json`: enam probe (konteks, skor, hukum, data sensitif, luar konteks, prompt injection).
- `AI-PROBE-STAGING.json`: jawaban live dari staging dan umpan balik.
- `screenshots-staging/01-konsultasi-jawaban.png` dan `02-log.png`.
- Model `gemini-3.5-flash-lite`; 3.8/3.6 Flash timeout dan 3.7 Flash 503 pada free tier saat diuji.

## Urutan berikutnya

1. Deploy staging Render + Vercel.
2. Jalankan UAT 5 Desember dan isi SUS.
3. Uji `pg_dump` dan restore penuh.
4. Bangun Must 3 dan 4.
5. Susun TCO 12 bulan.
6. Lengkapi 31 kriteria dan dashboard di P15.

## Aturan

- Jangan menulis hasil UAT atau skor SUS sebelum sesi 5 Desember.
- Jangan mengklaim backup terbukti penuh; yang sudah diuji baru salinan logis.
- Jangan menambah Must keenam.
