"""Drill backup dan restore logis ke schema terpisah.

Bukan pengganti pg_dump. Skrip ini menyalin setiap tabel public ke schema
`restore_drill`, membandingkan jumlah baris, lalu menghapus schema tersebut.

Jalankan:
    python db/backup_restore_drill.py
"""

from __future__ import annotations

import io
import os
import sys
from pathlib import Path

import psycopg

SCHEMA = "restore_drill"


def database_url() -> str:
    value = os.getenv("DATABASE_URL", "")
    if value:
        return value
    env = Path(__file__).resolve().parents[1] / "backend" / ".env"
    if not env.exists():
        raise SystemExit("DATABASE_URL tidak ditemukan.")
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.startswith("DATABASE_URL="):
            return line.split("=", 1)[1]
    raise SystemExit("DATABASE_URL tidak ditemukan.")


def main() -> int:
    url = database_url()
    with psycopg.connect(url, autocommit=True) as conn:
        tables = [
            row[0]
            for row in conn.execute(
                "select tablename from pg_tables where schemaname = 'public' order by tablename"
            ).fetchall()
        ]
        if not tables:
            raise SystemExit("Tidak ada tabel public.")

        conn.execute(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE")
        conn.execute(f"CREATE SCHEMA {SCHEMA}")

        total_source = 0
        total_restored = 0
        mismatches: list[str] = []
        print(f"Tabel: {len(tables)}")
        for table in tables:
            conn.execute(
                f'CREATE TABLE {SCHEMA}."{table}" '
                f'(LIKE public."{table}" INCLUDING ALL EXCLUDING IDENTITY)'
            )
            buffer = io.BytesIO()
            with conn.cursor() as cursor:
                with cursor.copy(f'COPY public."{table}" TO STDOUT') as copy:
                    for chunk in copy:
                        buffer.write(chunk)
            buffer.seek(0)
            with conn.cursor() as cursor:
                with cursor.copy(f'COPY {SCHEMA}."{table}" FROM STDIN') as copy:
                    while chunk := buffer.read(65536):
                        copy.write(chunk)
            source = conn.execute(f'select count(*) from public."{table}"').fetchone()[0]
            restored = conn.execute(f'select count(*) from {SCHEMA}."{table}"').fetchone()[0]
            total_source += source
            total_restored += restored
            status = "OK" if source == restored else "BEDA"
            if source != restored:
                mismatches.append(f"{table}: {source} -> {restored}")
            print(f"  {status:4} {table:24} {source:>5} baris")

        conn.execute(f"CREATE TABLE {SCHEMA}._tx_test (id integer)")
        try:
            with conn.transaction():
                conn.execute(f"INSERT INTO {SCHEMA}._tx_test VALUES (1)")
                raise RuntimeError("rollback disengaja")
        except RuntimeError:
            pass
        tx_rows = conn.execute(f"SELECT count(*) FROM {SCHEMA}._tx_test").fetchone()[0]

        print()
        print(f"Total baris sumber   : {total_source}")
        print(f"Total baris restore  : {total_restored}")
        print(f"Tabel berbeda        : {len(mismatches)}")
        print(f"Uji rollback transaksi: {'OK' if tx_rows == 0 else 'GAGAL'}")
        for item in mismatches:
            print("  -", item)

        conn.execute(f"DROP SCHEMA {SCHEMA} CASCADE")
        print("Schema drill dibersihkan.")

    return 0 if total_source == total_restored and tx_rows == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
