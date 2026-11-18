# Architecture Repository Growpath

Repositori arsitektur Kelompok 6 untuk proyek Growpath, platform advisory UMKM berbasis kecerdasan buatan. Repositori ini mengikuti struktur Architecture Repository pada panduan Sprint P13-P16.

## Status

- Fase: P13, pembekuan arsitektur dan desain sistem.
- Fokus: lima fitur Must, yaitu data usaha, konsultasi AI, rekomendasi, log jawaban AI, dan dashboard.
- Repositori ini berisi artefak arsitektur, bukan aplikasi produksi.
- Aplikasi MVP akan dibangun pada P14-P15 dan diuji pada P15.

## Struktur

| Folder | Isi |
|---|---|
| `00_Vision` | Visi, objek, pemangku kepentingan, piagam tim, ringkasan proyek |
| `01_Business` | Value chain, solution concept, BPMN, functional decomposition |
| `02_Data` | ERD, logical data model, kamus data |
| `03_Application` | Modul aplikasi, API landscape, kontrak OpenAPI |
| `04_Technology` | Topologi, deployment, SSO, API Gateway, infrastruktur |
| `05_Opportunities` | Gap analysis, roadmap, migration plan |
| `06_Governance` | ADR, change request log, compliance, team charter |
| `07_Evidence` | Rencana UAT, indeks bukti, bukti lapangan |
| `08_Source` | Repositori kode, changelog, panduan menjalankan |
| `09_Pitch` | Pitch deck dan materi demo |

## Aturan

- Setiap artefak mencantumkan penyusun dan peninjau.
- Perubahan lingkup harus melalui `06_Governance/CHANGE-REQUEST-LOG.md`.
- Keputusan teknologi dicatat sebagai ADR.
- Bukti kontribusi berupa commit, pull request, kartu papan kerja, dan notulen.

## Sumber

- `Progress Pertemuan 12 Kelompok 6 - Growpath.docx`
- `Ringkasan Proyek Growpath - Kelompok 6.docx`
- `Skenario_Project ASP R001.pdf`
