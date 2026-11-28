"""Backup dan restore logis PostgreSQL tanpa pg_dump.

Backup: salin setiap tabel public ke file COPY dan manifest.
Restore: buat schema terpisah, buat tabel LIKE public, lalu salin data.

Contoh:
    python db/backup_restore.py backup --out C:/Temp/growpath-backup
    python db/backup_restore.py restore --source C:/Temp/growpath-backup --schema restore_verify
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import psycopg

SCHEMA_RE = re.compile(r"^[a-z_][a-z0-9_]*$")


def database_url() -> str:
    value = os.getenv("DATABASE_URL", "")
    if value:
        return value
    env = Path(__file__).resolve().parents[1] / "backend" / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("DATABASE_URL="):
                return line.split("=", 1)[1]
    raise SystemExit("DATABASE_URL tidak ditemukan.")


def quote(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def list_tables(conn: psycopg.Connection) -> list[str]:
    return [
        row[0]
        for row in conn.execute(
            "select tablename from pg_tables where schemaname='public' order by tablename"
        ).fetchall()
    ]


def backup(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    url = database_url()
    with psycopg.connect(url, autocommit=True) as conn:
        tables = list_tables(conn)
        manifest = {
            "created_at": datetime.now(UTC).isoformat(),
            "database": conn.execute("select current_database()").fetchone()[0],
            "tables": [],
        }
        for table in tables:
            target = out_dir / f"{table}.copy"
            with conn.cursor() as cursor:
                with cursor.copy(f"COPY public.{quote(table)} TO STDOUT") as copy:
                    with target.open("wb") as handle:
                        for chunk in copy:
                            handle.write(chunk)
            count = conn.execute(
                f"select count(*) from public.{quote(table)}"
            ).fetchone()[0]
            manifest["tables"].append({"name": table, "rows": count})
            print(f"  {table:24} {count:>6} baris")
        (out_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
    print(f"Backup selesai: {out_dir}")
    return 0


def restore(source: Path, schema: str, keep: bool) -> int:
    if not SCHEMA_RE.match(schema):
        raise SystemExit("Nama schema tidak valid.")
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    url = database_url()
    mismatches: list[str] = []
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute(f"DROP SCHEMA IF EXISTS {quote(schema)} CASCADE")
        conn.execute(f"CREATE SCHEMA {quote(schema)}")
        for item in manifest["tables"]:
            table = item["name"]
            conn.execute(
                f"CREATE TABLE {quote(schema)}.{quote(table)} "
                f"(LIKE public.{quote(table)} INCLUDING ALL EXCLUDING IDENTITY)"
            )
            data = source / f"{table}.copy"
            with conn.cursor() as cursor:
                with cursor.copy(
                    f"COPY {quote(schema)}.{quote(table)} FROM STDIN"
                ) as copy:
                    with data.open("rb") as handle:
                        while chunk := handle.read(65536):
                            copy.write(chunk)
            source_count = int(item["rows"])
            restored_count = conn.execute(
                f"select count(*) from {quote(schema)}.{quote(table)}"
            ).fetchone()[0]
            status = "OK" if source_count == restored_count else "BEDA"
            if source_count != restored_count:
                mismatches.append(f"{table}: {source_count} -> {restored_count}")
            print(f"  {status:4} {table:24} {restored_count:>6} baris")

        if not keep:
            conn.execute(f"DROP SCHEMA {quote(schema)} CASCADE")
            print("Schema restore dibersihkan.")

    print(f"Tabel berbeda: {len(mismatches)}")
    for item in mismatches:
        print("  -", item)
    return 0 if not mismatches else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    backup_parser = sub.add_parser("backup")
    backup_parser.add_argument("--out", required=True)

    restore_parser = sub.add_parser("restore")
    restore_parser.add_argument("--source", required=True)
    restore_parser.add_argument("--schema", default="restore_verify")
    restore_parser.add_argument("--keep", action="store_true")

    args = parser.parse_args()
    if args.command == "backup":
        return backup(Path(args.out))
    return restore(Path(args.source), args.schema, args.keep)


if __name__ == "__main__":
    sys.exit(main())
