#!/usr/bin/env bash
# =============================================================================
# GROWPATH — SKRIP BACKUP & VERIFIKASI RESTORE POSTGRESQL (P13 -> P15)
# =============================================================================
# Proyek       : Growpath — Platform Advisory UMKM Berbasis AI (Kelompok 6)
# Disusun oleh : Wisnu Nugroho (F1E124032) — Database Architect
# Direview oleh: Moch Haikal Ramadhan (DevOps), Bagas Adinata (Programmer)
# Tanggal      : 22 November 2026
#
# Cara pakai:
#   1. Siapkan variabel lingkungan (JANGAN commit file .env ke Git):
#        export DATABASE_URL="postgresql://user:pass@host:5432/growpath"
#   2. Jalankan backup:
#        bash P13-Backup-Script-Wisnu-v01.sh backup
#   3. Jalankan uji restore ke database salinan (simulasi insiden P15):
#        export RESTORE_DATABASE_URL="postgresql://user:pass@host:5432/growpath_restore_test"
#        bash P13-Backup-Script-Wisnu-v01.sh restore backups/growpath_YYYYMMDD_HHMMSS.dump
# =============================================================================

set -euo pipefail

ACTION="${1:-backup}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP="$(date -u +%Y%m%d_%H%M%S)"
RETENTION_DAYS="${RETENTION_DAYS:-14}"

require_cmd() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "[ERROR] Perintah '$1' tidak ditemukan. Instal postgresql-client terlebih dahulu." >&2
        exit 1
    fi
}

do_backup() {
    require_cmd pg_dump
    if [[ -z "${DATABASE_URL:-}" ]]; then
        echo "[ERROR] Variabel DATABASE_URL belum disetel. Muat dari .env lokal (jangan hardcode di skrip)." >&2
        exit 1
    fi

    mkdir -p "$BACKUP_DIR"
    local dump_file="${BACKUP_DIR}/growpath_${TIMESTAMP}.dump"
    local sha_file="${dump_file}.sha256"

    echo "[INFO] Memulai backup PostgreSQL ke ${dump_file}..."
    pg_dump \
        --format=custom \
        --compress=6 \
        --no-owner \
        --no-privileges \
        --verbose \
        --file="$dump_file" \
        "$DATABASE_URL"

    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$dump_file" > "$sha_file"
        echo "[INFO] Checksum tersimpan di ${sha_file}."
    fi

    # Bersihkan backup lama melebihi masa retensi lokal
    find "$BACKUP_DIR" -type f -name "growpath_*.dump*" -mtime +"$RETENTION_DAYS" -delete || true

    echo "[OK] Backup selesai: ${dump_file} ($(du -h "$dump_file" | cut -f1))"
}

do_restore() {
    require_cmd pg_restore
    require_cmd psql
    local dump_file="${2:-}"

    if [[ -z "$dump_file" || ! -f "$dump_file" ]]; then
        echo "[ERROR] File backup tidak ditemukan. Pakai: $0 restore <path_file.dump>" >&2
        exit 1
    fi
    if [[ -z "${RESTORE_DATABASE_URL:-}" ]]; then
        echo "[ERROR] Variabel RESTORE_DATABASE_URL belum disetel (wajib arahkan ke DB salinan, bukan produksi)." >&2
        exit 1
    fi

    if [[ -f "${dump_file}.sha256" ]] && command -v sha256sum >/dev/null 2>&1; then
        echo "[INFO] Memverifikasi checksum SHA-256..."
        sha256sum -c "${dump_file}.sha256"
    fi

    local start_ts
    start_ts="$(date +%s)"
    echo "[INFO] Memulai restore ke database uji (RESTORE_DATABASE_URL)..."

    pg_restore \
        --clean \
        --if-exists \
        --no-owner \
        --no-privileges \
        --exit-on-error \
        --dbname="$RESTORE_DATABASE_URL" \
        "$dump_file"

    local end_ts elapsed
    end_ts="$(date +%s)"
    elapsed=$((end_ts - start_ts))

    echo "[INFO] Memverifikasi jumlah tabel dan baris inti hasil restore..."
    psql "$RESTORE_DATABASE_URL" -c "
        SELECT 'tenants' AS tabel, count(*) AS baris FROM tenants
        UNION ALL SELECT 'users', count(*) FROM users
        UNION ALL SELECT 'umkm_profiles', count(*) FROM umkm_profiles
        UNION ALL SELECT 'criteria', count(*) FROM criteria
        UNION ALL SELECT 'assessments', count(*) FROM assessments
        UNION ALL SELECT 'ai_consultations', count(*) FROM ai_consultations
        UNION ALL SELECT 'ai_response_logs', count(*) FROM ai_response_logs
        UNION ALL SELECT 'ai_usage_quotas', count(*) FROM ai_usage_quotas
        ORDER BY tabel;
    "

    echo "[OK] Uji restore selesai dalam ${elapsed} detik."
}

case "$ACTION" in
    backup)
        do_backup
        ;;
    restore)
        do_restore "$@"
        ;;
    *)
        echo "Penggunaan: $0 {backup|restore <file.dump>}" >&2
        exit 1
        ;;
esac