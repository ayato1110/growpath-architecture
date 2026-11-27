# P14 · Log Eksekusi Database dan Smoke Test

**Tanggal:** 27 November 2026  
**Lingkungan:** Windows, Python 3.12.5, Node 24.14.1  
**Database:** Supabase PostgreSQL 17.12, project `growpath`, ref `xckzrccbxxkisrbtrdmx`, region Seoul (ap-northeast-2)  
**Backend lokal:** port 8001 (port 8000 dipakai proses lain di mesin)  
**Frontend lokal:** port 3000

## Perintah yang dijalankan

```bash
python 08_Source/db/run_sql.py \
  08_Source/db/migrations/001_init.sql \
  08_Source/db/seed/seed.sql \
  08_Source/db/migrations/002_p14.sql \
  08_Source/db/verify_p14.sql --yes
```

```bash
API_BASE_URL=http://127.0.0.1:8001 \
SMOKE_EMAIL=... SMOKE_PASSWORD=... \
SMOKE_OTHER_EMAIL=... SMOKE_OTHER_PASSWORD=... \
python 08_Source/tests/p14_smoke.py \
  --report 07_Evidence/P14/smoke-report.json
```

## Hasil

| Pemeriksaan | Hasil |
|---|---|
| Koneksi Supabase | OK, PostgreSQL 17.12 |
| `001_init.sql` | OK, 160 statement |
| `seed.sql` | OK, 14 statement |
| `002_p14.sql` | OK, 4 statement |
| `verify_p14.sql` | OK, tanpa exception |
| Smoke test | 15 lulus, 0 gagal, 2 skip |
| Skor contoh | 47,92, segmen Branding Enthusiasts |
| Cakupan | 12 dari 31 kriteria, 2 dimensi |
| Roadmap | 3 langkah, status selesai bertahan setelah muat ulang |

Ringkasan database ada di `db-verify.txt`. Tangkapan layar ada di `screenshots/`.

## Bug yang ditemukan dan diperbaiki saat verifikasi

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| Semua endpoint data 500, `No module named psycopg2` | SQLAlchemy memilih driver psycopg2 dari URL `postgresql://` | `core/db.py` mengubah URL ke `postgresql+psycopg://` |
| Simpan jawaban 500, `'function' object has no attribute 'excluded'` | Memakai `insert.excluded`, bukan objek statement | Statement disimpan di variabel sebelum `on_conflict_do_update` |
| Submit 500, milestone melanggar foreign key | Milestone di-insert sebelum roadmap di-flush | `session.flush()` setelah menambah roadmap |
| Asesmen sudah `scored` tetapi roadmap tidak dibuat | Pembuatan roadmap hanya di dalam blok scoring | Roadmap dipastikan ada di luar blok, termasuk saat submit ulang |

## Catatan

- Port 8000 dipakai `php.exe` milik proyek lain; backend P14 memakai 8001 pada pengujian ini.
- `BACKEND_URL` di `frontend/.env.local` diubah ke 8001 hanya untuk pengujian lokal dan tidak di-commit.
- Kredensial database dan akun uji tidak ditulis di dokumen ini.
- TC-03 lulus pada run pertama (profil kosong menjawab 404); pada run berikutnya di-skip karena profil sudah ada.
- TC-07 belum dijalankan otomatis; butuh akun UMKM tanpa profil dan pemeriksaan redirect di UI.
