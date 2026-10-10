import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

import psycopg
import pytest

from backend import job

START = datetime(2030, 1, 1, 21, 17, tzinfo=timezone.utc)


def test_recover_seven_hour_gap_and_repeat(monkeypatch, capsys):
    completed = {START}
    calls = []
    monkeypatch.setattr(job, "completed_slots", lambda start, end: completed.copy())

    def record(key, slot):
        calls.append(slot)
        completed.add(slot)
        return True

    monkeypatch.setattr(job, "run", record)
    now = START + timedelta(hours=7, minutes=5)
    assert job.recover(now, 24, START) == 0
    assert calls == [START + timedelta(hours=i) for i in range(1, 8)]
    assert job.recover(now, 24, START) == 0
    assert len(calls) == 7
    assert "'pending_remaining': 0" in capsys.readouterr().out


def test_limit_leaves_older_slots_for_next_run(monkeypatch, capsys):
    completed = set()
    monkeypatch.setattr(job, "completed_slots", lambda start, end: completed.copy())

    def record(key, slot):
        completed.add(slot)
        return True

    monkeypatch.setattr(job, "run", record)
    now = START + timedelta(hours=6, minutes=5)
    assert job.recover(now, 3, START) == 4
    assert completed == {START + timedelta(hours=i) for i in range(3)}
    assert job.recover(now, 3, START) == 1
    assert job.recover(now, 3, START) == 0
    assert "'pending_remaining': 4" in capsys.readouterr().out


def test_no_missing_slots(monkeypatch):
    now = START + timedelta(hours=2)
    monkeypatch.setattr(
        job,
        "completed_slots",
        lambda start, end: {START + timedelta(hours=i) for i in range(3)},
    )
    monkeypatch.setattr(job, "run", lambda key, slot: pytest.fail("unexpected run"))
    assert job.recover(now, 2, START) == 0
    assert job.pending_slots(START - timedelta(minutes=1), START) == []


def test_failure_does_not_complete_failed_or_later_slots(monkeypatch, capsys):
    completed = set()
    monkeypatch.setattr(job, "completed_slots", lambda start, end: completed.copy())

    def record(key, slot):
        if slot == START + timedelta(hours=2):
            raise RuntimeError("synthetic failure")
        completed.add(slot)
        return True

    monkeypatch.setattr(job, "run", record)
    with pytest.raises(RuntimeError, match="synthetic failure"):
        job.recover(START + timedelta(hours=4), 5, START)
    assert completed == {START, START + timedelta(hours=1)}
    assert "'pending_at_start_after_failure': 3" in capsys.readouterr().out


def test_utc_day_change(monkeypatch):
    start = datetime(2030, 1, 1, 23, 17, tzinfo=timezone.utc)
    monkeypatch.setattr(job, "completed_slots", lambda first, end: set())
    assert job.pending_slots(start + timedelta(hours=2), start) == [
        start,
        datetime(2030, 1, 2, 0, 17, tzinfo=timezone.utc),
        datetime(2030, 1, 2, 1, 17, tzinfo=timezone.utc),
    ]


@pytest.mark.skipif(
    not os.getenv("POC_TEST_DATABASE_URL"), reason="PostgreSQL de teste não configurado"
)
def test_database_gap_and_concurrent_execution(monkeypatch):
    url = os.environ["POC_TEST_DATABASE_URL"]
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("POC_DB_SSLMODE", "disable")
    start = datetime(2031, 1, 1, 21, 17, tzinfo=timezone.utc)
    end = start + timedelta(hours=2)
    with psycopg.connect(url, sslmode="disable") as conn, conn.cursor() as cur:
        cur.execute(Path("backend/schema.sql").read_text(encoding="utf-8"))
        cur.execute(
            "DELETE FROM poc_job_runs WHERE scheduled_at BETWEEN %s AND %s",
            (start, end),
        )
    try:
        assert job.run(f"poc-hourly-{start:%Y%m%d%H}", start)
        assert job.pending_slots(end, start) == [
            start + timedelta(hours=1),
            end,
        ]
        slot = start + timedelta(hours=1)
        key = f"poc-hourly-{slot:%Y%m%d%H}"
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: job.run(key, slot), range(2)))
        assert sorted(results) == [False, True]
        assert job.recover(end, 1, start) == 0
        with psycopg.connect(url, sslmode="disable") as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT count(*) FROM poc_job_runs WHERE scheduled_at BETWEEN %s AND %s",
                (start, end),
            )
            assert cur.fetchone()[0] == 3
    finally:
        with psycopg.connect(url, sslmode="disable") as conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM poc_job_runs WHERE scheduled_at BETWEEN %s AND %s",
                (start, end),
            )
