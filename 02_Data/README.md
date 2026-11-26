# 02_Data

Folder ini memuat arsitektur data P13.

## P13

- `P13-31-Kriteria.md` - katalog 31 kriteria
- `P13-31-Kriteria-Asumsi.md` - asumsi bobot, poin, segmen, dan rencana validasi
- `erd-3nf.md` - ERD konseptual ke logis dan bukti 3NF
- `kamus-data-p13.md` - kamus data 23 entitas
- `seed-data.md` - penjelasan data uji
- `P13-Backup-Script-Wisnu-v01.sh` - backup dan verifikasi restore
- `diagrams/erd-3nf.drawio` - sumber ERD
- `diagrams/erd-inti.png`
- `diagrams/erd-katalog-jawaban.png`
- `diagrams/erd-advisory-ai.png`
- `diagrams/erd-pendukung-fase2.png`

DDL: `../08_Source/db/migrations/001_init.sql`.
Seed: `../08_Source/db/seed/seed.sql`.

Data uji adalah data sintetis. Skor tidak diisi di seed; skor dihitung Scoring Service.
