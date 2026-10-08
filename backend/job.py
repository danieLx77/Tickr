"""Job sintético idempotente com recuperação de horários lógicos ausentes."""

import argparse
import os
from datetime import datetime, timedelta, timezone

import psycopg


def run(logical_key: str, scheduled_at: datetime) -> bool:
    url = os.environ["DATABASE_URL"]
    with (
        psycopg.connect(
            url, connect_timeout=5, sslmode=os.getenv("POC_DB_SSLMODE", "require")
        ) as conn,
        conn.cursor() as cur,
    ):
        cur.execute(
            "INSERT INTO poc_job_runs (logical_key, scheduled_at, status) VALUES (%s, %s, 'completed') ON CONFLICT (logical_key) DO NOTHING RETURNING logical_key",
            (logical_key, scheduled_at),
        )
        return cur.fetchone() is not None


def expected_slots(now: datetime, hours: int) -> list[datetime]:
    latest = now.astimezone(timezone.utc).replace(minute=17, second=0, microsecond=0)
    if latest > now.astimezone(timezone.utc):
        latest -= timedelta(hours=1)
    return [latest - timedelta(hours=offset) for offset in reversed(range(hours))]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--key")
    group.add_argument("--recover-hours", type=int)
    parser.add_argument("--scheduled-at")
    args = parser.parse_args()
    if args.recover_hours is not None:
        if not 1 <= args.recover_hours <= 24:
            parser.error("recover-hours deve estar entre 1 e 24")
        slots = expected_slots(datetime.now(timezone.utc), args.recover_hours)
        jobs = [(f"poc-hourly-{slot:%Y%m%d%H}", slot) for slot in slots]
    else:
        if not args.scheduled_at:
            parser.error("scheduled-at é obrigatório com --key")
        scheduled_at = datetime.fromisoformat(args.scheduled_at.replace("Z", "+00:00"))
        if scheduled_at.tzinfo is None:
            parser.error("scheduled-at precisa de fuso horário")
        jobs = [(args.key, scheduled_at)]
    for key, planned in jobs:
        inserted = run(key, planned)
        print(
            {
                "logical_key": key,
                "scheduled_at": planned.isoformat(),
                "executed_at": datetime.now(timezone.utc).isoformat(),
                "inserted": inserted,
            }
        )
