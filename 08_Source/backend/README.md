# Backend

Folder ini disiapkan untuk FastAPI dan Pydantic v2.

Struktur final ada di [`../../03_Application/P13-App-Structure.md`](../../03_Application/P13-App-Structure.md).

Aturan utama:

- `api/` hanya menangani HTTP.
- `services/` memuat aturan bisnis, skor, rekomendasi, dan AI.
- `repositories/` adalah satu-satunya lapisan yang mengakses database.
- `models/` memakai SQLAlchemy 2.x.
- `alembic/` mengelola migrasi.
- `tenant_id` dan `user_id` diambil dari JWT.

Scaffold FastAPI, login, role, dan health check sudah ada. Fitur P14-P15 menyusul.
