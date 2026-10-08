#!/usr/bin/env bash
set -euo pipefail
: "${DATABASE_URL:?DATABASE_URL ausente}"
: "${BACKUP_PASSPHRASE:?BACKUP_PASSPHRASE ausente}"
: "${BACKUP_OUTPUT_DIR:?BACKUP_OUTPUT_DIR ausente}"
mkdir -p "$BACKUP_OUTPUT_DIR"
backup_stamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_file="$BACKUP_OUTPUT_DIR/tickr-poc-$backup_stamp.dump.enc"
plain_file="$(mktemp)"
trap 'rm -f "$plain_file"' EXIT
pg_dump --format=custom --no-owner --no-acl --dbname="$DATABASE_URL" --file="$plain_file"
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 250000 -in "$plain_file" -out "$backup_file" -pass env:BACKUP_PASSPHRASE
(cd "$BACKUP_OUTPUT_DIR" && sha256sum "$(basename "$backup_file")" > "$(basename "$backup_file").sha256")
(cd "$BACKUP_OUTPUT_DIR" && sha256sum --check "$(basename "$backup_file").sha256")
printf 'Backup criptografado criado: %s\n' "$backup_file"
