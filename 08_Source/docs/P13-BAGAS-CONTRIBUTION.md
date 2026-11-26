# Kontribusi Bagas P13

**Pemilik:** Bagas Adinata
**Peran:** Programmer
**Tanggal:** 23 November 2026

## 1. Lingkup

- P13-12 Pola aplikasi dan struktur folder.
- P13-13 Repo dan branch `main/dev/feature`.
- PR14-06 Aplikasi lokal dengan login dan role.
- PR14-07 README cara menjalankan.
- Test matriks role untuk backend.

## 2. P13-12 dan P13-13

- Dokumen pola aplikasi: `03_Application/P13-App-Structure.md`.
- ADR: `06_Governance/ADR-002-application-structure.md`.
- Struktur kode: `08_Source/frontend`, `08_Source/backend`, `08_Source/db`, `08_Source/infra`, `08_Source/tests`, `08_Source/docs`.
- Branch: `main` untuk rilis, `dev` untuk integrasi, `feature/*`/`docs/*` untuk pekerjaan.

## 3. PR14-06 dan PR14-07

- Frontend Next.js: `08_Source/frontend`.
- Backend FastAPI: `08_Source/backend`.
- Login dan role lokal: `/auth/login`, `/auth/me`, cookie sesi.
- Health check: `/health`.
- README cara menjalankan: `08_Source/README.md`.
- Bukti login: `07_Evidence/PR14-06/` dan `07_Evidence/PR14-06-Login-Role.md`.

## 4. Test matriks role

File: `08_Source/backend/tests/test_roles_matrix.py`.

Test memeriksa:

- Setiap role boleh mengakses endpoint yang memakai role yang sama.
- Role lain ditolak dengan `403` dan kode `AUTH_ROLE_REQUIRED`.
- Lima role: `umkm`, `pendamping`, `mentor`, `admin_b2g`, `admin_platform`.

Hasil:

```text
25 passed, 5 skipped
```

Perintah:

```bash
cd 08_Source/backend
.venv/Scripts/python -m pytest -q tests/test_roles_matrix.py
```

## 5. Batas

- Ini test lokal, bukan UAT.
- Belum ada deployment live.
- Fitur bisnis P14 belum dibangun.
