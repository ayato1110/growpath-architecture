# Changelog

## Unreleased

- Struktur repositori arsitektur dibuat.
- P13: menetapkan pola aplikasi, struktur folder, dan strategi branch.
- P13: menambahkan placeholder `frontend`, `backend`, `infra`, `tests`, dan `docs`.
- P13: menambahkan `03_Application/P13-App-Structure.md` dan `06_Governance/ADR-002-application-structure.md`.
- Aplikasi lokal login dan role (PR14-06): frontend Next.js, backend FastAPI, mode local, route `/app` terlindungi. Pull request #14.
- README cara menjalankan (PR14-07): prasyarat, env, port lokal, tes, dan troubleshooting. Pull request #14.
- P13 database: menambahkan `db/migrations/001_init.sql` dan `db/seed/seed.sql` dari artefak data Wisnu.
- P14 data usaha: form 10 field demografi, validasi backend, dan penyimpanan PostgreSQL.
- P14 asesmen: draf Psikografi dan Pasar, 12 kriteria, simpan jawaban, tinjau.
- P14 rekomendasi: skor deterministik, segmen, cakupan 12/31, dan tiga langkah prioritas berbasis aturan.
- P14 database: `db/migrations/002_p14.sql` (view `v_assessment_report`), `db/verify_p14.sql`, dan pemetaan akun lokal ke tabel `user`.
- P14 staging: `render.yaml` dan `04_Technology/P14-Staging-Deployment.md`.
- P14 bukti: 15 test case, skrip smoke test, audit kontribusi, dan checklist Gate 2 di `07_Evidence/P14/`.
- P15: konsultasi AI Gemini 3.8 Flash, guardrail, kuota 10/hari, log jawaban, dan umpan balik.
- Fitur dashboard dibangun setelah ini.
