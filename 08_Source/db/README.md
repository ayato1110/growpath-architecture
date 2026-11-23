# Database

Folder ini memuat skema dan seed PostgreSQL P13.

```text
db/
  migrations/001_init.sql
  seed/seed.sql
```

## Menjalankan

Dari root repo:

```bash
psql "$DATABASE_URL" -f 08_Source/db/migrations/001_init.sql
psql "$DATABASE_URL" -f 08_Source/db/seed/seed.sql
```

Aturan:

- `001_init.sql` menghapus objek Growpath yang sudah ada sebelum membuat ulang. Jalankan hanya di database kosong atau database uji.
- `seed.sql` memuat data uji, bukan data produksi.
- Skor tidak diisi di seed. Skor dihitung Scoring Service.
- Bukti eksekusi ada di `07_Evidence/DDL.png`, `07_Evidence/SEED.png`, dan uji RLS di `07_Evidence/`.

Rujukan:

- `02_Data/erd-3nf.md`
- `02_Data/kamus-data-p13.md`
- `02_Data/seed-data.md`
- `02_Data/P13-31-Kriteria.md`
