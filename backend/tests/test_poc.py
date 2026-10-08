import os
from datetime import datetime, timezone
from pathlib import Path

import psycopg
import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.job import expected_slots, run

client = TestClient(app)


def test_health_and_unauthorized_write(monkeypatch):
    monkeypatch.setenv("POC_WRITE_TOKEN", "synthetic-local-secret")
    assert client.get("/health").json() == {"status": "ok", "phase": "00"}
    assert (
        client.post("/records", json={"key": "demo", "value": "x"}).status_code == 401
    )
    assert client.post("/transaction-check").status_code == 401
    assert client.get("/records/invalid!key").status_code == 422


def test_database_unavailable(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert client.get("/db").status_code == 503
    assert "DATABASE_URL" not in client.get("/db").text


@pytest.mark.skipif(
    not os.getenv("POC_TEST_DATABASE_URL"), reason="PostgreSQL de teste não configurado"
)
def test_database_read_write_transaction_and_job(monkeypatch):
    url = os.environ["POC_TEST_DATABASE_URL"]
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("POC_WRITE_TOKEN", "synthetic-local-secret")
    monkeypatch.setenv("POC_DB_SSLMODE", "disable")
    with psycopg.connect(url, sslmode="disable") as conn, conn.cursor() as cur:
        cur.execute(Path("backend/schema.sql").read_text(encoding="utf-8"))
        cur.execute("DELETE FROM poc_records WHERE key IN ('demo', 'rollback_probe')")
        cur.execute("DELETE FROM poc_job_runs WHERE logical_key = 'test-logical-key'")
    assert client.get("/db").json() == {"connected": True}
    response = client.post(
        "/records",
        headers={"Authorization": "Bearer synthetic-local-secret"},
        json={"key": "demo", "value": "synthetic"},
    )
    assert response.status_code == 201
    assert client.get("/records/demo").json()["value"] == "synthetic"
    assert client.post(
        "/transaction-check", headers={"Authorization": "Bearer synthetic-local-secret"}
    ).json() == {"rollback_ok": True}
    scheduled = datetime(2026, 10, 8, 12, 0, tzinfo=timezone.utc)
    assert run("test-logical-key", scheduled) is True
    assert run("test-logical-key", scheduled) is False
    with psycopg.connect(url, sslmode="disable") as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM poc_job_runs WHERE logical_key = 'test-logical-key'"
        )
        assert cur.fetchone()[0] == 1
        cur.execute("SELECT count(*) FROM poc_records WHERE key = 'rollback_probe'")
        assert cur.fetchone()[0] == 0


def test_expected_slots_for_recovery():
    slots = expected_slots(datetime(2026, 10, 8, 13, 5, tzinfo=timezone.utc), 3)
    assert [slot.isoformat() for slot in slots] == [
        "2026-10-08T10:17:00+00:00",
        "2026-10-08T11:17:00+00:00",
        "2026-10-08T12:17:00+00:00",
    ]
