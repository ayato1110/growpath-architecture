# QA Bagas P13

**Tanggal:** 23 November 2026
**Pemilik:** Bagas Adinata
**Scope:** P13-12, P13-13, PR14-06, PR14-07

## Checklist

- [x] Struktur `08_Source/frontend`, `backend`, `db`, `infra`, `tests`, `docs` ada.
- [x] Frontend Next.js dan backend FastAPI bisa dijalankan lokal.
- [x] Login `/login` berfungsi.
- [x] Route `/app` terlindungi.
- [x] Role lokal tersedia: umkm, pendamping, mentor, admin_b2g, admin_platform.
- [x] `/health` tersedia.
- [x] README cara menjalankan ada.
- [x] Test matriks role lulus.
- [ ] Live deployment belum dilakukan.
- [ ] UAT belum dilakukan.

## Test

File: `08_Source/backend/tests/test_roles_matrix.py`

Perintah:

```bash
cd 08_Source/backend
.venv/Scripts/python -m pytest -q tests/test_roles_matrix.py
```

Hasil:

```text
25 passed, 5 skipped
```

## Catatan

- Screenshot login dan `/app` ada di folder ini.
- Ini test lokal, bukan UAT.
- Jobdesc topologi/hosting/NFR tetap milik Haikal, tidak dimasukkan ke folder Bagas.
