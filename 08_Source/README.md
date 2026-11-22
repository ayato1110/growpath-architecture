# 08_Source

Folder ini memuat kode aplikasi, struktur kerja, changelog, dan panduan menjalankan.

Status P13: pola aplikasi, struktur folder, dan branch sudah ditetapkan. Kode fitur MVP dibangun P14-P15.

## Struktur

```text
08_Source/
  frontend/       Next.js App Router dan TypeScript
  backend/        FastAPI, Pydantic v2, SQLAlchemy, Alembic
  infra/          Docker, Railway, dan script operasional
  tests/          E2E Playwright dan fixture
  docs/           Catatan implementasi
  README.md
  CHANGELOG.md
```

Dokumen lengkap: [`../03_Application/P13-App-Structure.md`](../03_Application/P13-App-Structure.md).

## Branch

- `main` untuk rilis, gate, demo, dan submission.
- `dev` untuk integrasi harian. Semua pull request mengarah ke `dev`.
- `feature/<topik>` untuk fitur aplikasi.
- `docs/<topik>` untuk dokumen dan struktur.
- `hotfix/<topik>` untuk perbaikan mendesak dari `main`, lalu kembali ke `dev`.

Jangan push langsung ke `main` atau `dev`. Aturan lengkap ada di [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Batas P13 dan Session 4

P13 menetapkan pola, struktur folder, kontrak API, dan branch. Session 4 mengerjakan scaffold Next.js/FastAPI, login, role, form data usaha, health check, README cara menjalankan, tes awal, dan bukti build.

Kode fitur tidak ditulis di P13.
