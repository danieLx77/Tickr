"""Job sintético idempotente com recuperação de horários lógicos ausentes."""

import argparse
import os
from datetime import datetime, timedelta, timezone

import psycopg

FIRST_SCHEDULED_AT = datetime(2026, 10, 8, 21, 17, tzinfo=timezone.utc)


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
        if cur.fetchone() is not None:
            return True
        cur.execute(
            "SELECT scheduled_at, status FROM poc_job_runs WHERE logical_key = %s",
            (logical_key,),
        )
        existing_at, status = cur.fetchone()
        if existing_at != scheduled_at or status != "completed":
            raise ValueError(f"chave lógica conflitante: {logical_key}")
        return False


def latest_slot(now: datetime) -> datetime:
    latest = now.astimezone(timezone.utc).replace(minute=17, second=0, microsecond=0)
    if latest > now.astimezone(timezone.utc):
        latest -= timedelta(hours=1)
    return latest


def completed_slots(start: datetime, end: datetime) -> set[datetime]:
    url = os.environ["DATABASE_URL"]
    with (
        psycopg.connect(
            url, connect_timeout=5, sslmode=os.getenv("POC_DB_SSLMODE", "require")
        ) as conn,
        conn.cursor() as cur,
    ):
        cur.execute(
            "SELECT logical_key, scheduled_at FROM poc_job_runs "
            "WHERE logical_key LIKE 'poc-hourly-%%' AND scheduled_at BETWEEN %s AND %s "
            "AND status = 'completed'",
            (start, end),
        )
        return {
            scheduled_at
            for key, scheduled_at in cur.fetchall()
            if key == f"poc-hourly-{scheduled_at:%Y%m%d%H}"
        }


def pending_slots(now: datetime, start: datetime = FIRST_SCHEDULED_AT) -> list[datetime]:
    end = latest_slot(now)
    if end < start:
        return []
    completed = completed_slots(start, end)
    slots = []
    slot = start
    while slot <= end:
        if slot not in completed:
            slots.append(slot)
        slot += timedelta(hours=1)
    return slots


def recover(now: datetime, limit: int, start: datetime = FIRST_SCHEDULED_AT) -> int:
    if limit < 1:
        raise ValueError("recover-limit deve ser positivo")
    pending = pending_slots(now, start)
    for processed, slot in enumerate(pending[:limit]):
        key = f"poc-hourly-{slot:%Y%m%d%H}"
        try:
            inserted = run(key, slot)
        except Exception:
            print(
                {
                    "pending_at_start_after_failure": len(pending) - processed,
                    "failed_at": slot.isoformat(),
                },
                flush=True,
            )
            raise
        print(
            {
                "logical_key": key,
                "scheduled_at": slot.isoformat(),
                "executed_at": datetime.now(timezone.utc).isoformat(),
                "inserted": inserted,
            },
            flush=True,
        )
    remaining = len(pending_slots(now, start))
    print({"pending_remaining": remaining}, flush=True)
    return remaining


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--key")
    group.add_argument("--recover", action="store_true")
    parser.add_argument("--scheduled-at")
    parser.add_argument("--recover-limit", type=int, default=24)
    args = parser.parse_args()
    if args.recover:
        if args.recover_limit < 1:
            parser.error("recover-limit deve ser positivo")
        recover(datetime.now(timezone.utc), args.recover_limit)
    else:
        if not args.scheduled_at:
            parser.error("scheduled-at é obrigatório com --key")
        scheduled_at = datetime.fromisoformat(args.scheduled_at.replace("Z", "+00:00"))
        if scheduled_at.tzinfo is None:
            parser.error("scheduled-at precisa de fuso horário")
        inserted = run(args.key, scheduled_at)
        print(
            {
                "logical_key": args.key,
                "scheduled_at": scheduled_at.isoformat(),
                "executed_at": datetime.now(timezone.utc).isoformat(),
                "inserted": inserted,
            }
        )
