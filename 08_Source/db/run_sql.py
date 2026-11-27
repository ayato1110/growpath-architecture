"""Jalankan file SQL ke PostgreSQL tanpa psql.

Contoh:
    python db/run_sql.py db/migrations/001_init.sql db/seed/seed.sql db/migrations/002_p14.sql --yes

Membaca DATABASE_URL dari environment bila --url tidak diisi.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pglast
import psycopg


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="File SQL yang dijalankan berurutan.")
    parser.add_argument("--url", default=os.getenv("DATABASE_URL", ""))
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Lewati konfirmasi. Wajib untuk 001_init.sql karena menghapus tabel.",
    )
    args = parser.parse_args()

    if not args.url:
        print("DATABASE_URL belum diisi.", file=sys.stderr)
        return 2

    targets = [Path(item) for item in args.files]
    missing = [str(item) for item in targets if not item.exists()]
    if missing:
        print("File tidak ditemukan: " + ", ".join(missing), file=sys.stderr)
        return 2

    if not args.yes:
        print("Skrip ini dapat menghapus dan membuat ulang tabel.")
        print("Ketik 'ya' untuk melanjutkan: ", end="", flush=True)
        if input().strip().lower() != "ya":
            print("Dibatalkan.")
            return 1

    with psycopg.connect(args.url, autocommit=True) as connection:
        for target in targets:
            sql = target.read_text(encoding="utf-8")
            statements = [stmt for stmt in pglast.split(sql) if stmt.strip()]
            for index, statement in enumerate(statements, start=1):
                try:
                    connection.execute(statement)
                except psycopg.Error as exc:
                    print(
                        f"GAGAL {target} statement {index}: {exc}",
                        file=sys.stderr,
                    )
                    return 1
            print(f"OK {target} ({len(statements)} statement)")

    print("Selesai.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
