#!/usr/bin/env bash
set -euo pipefail
: "${RESTORE_DATABASE_URL:?RESTORE_DATABASE_URL ausente}"
: "${BACKUP_PASSPHRASE:?BACKUP_PASSPHRASE ausente}"
backup_file="${1:?Informe arquivo .dump.enc}"
sha256sum --check "$backup_file.sha256"
plain_file="$(mktemp)"
trap 'rm -f "$plain_file"' EXIT
openssl enc -d -aes-256-cbc -pbkdf2 -iter 250000 -in "$backup_file" -out "$plain_file" -pass env:BACKUP_PASSPHRASE
pg_restore --exit-on-error --single-transaction --no-owner --no-acl --dbname="$RESTORE_DATABASE_URL" "$plain_file"
printf 'Restauração isolada concluída; valide os registros com uma consulta ao banco de destino.\n'
