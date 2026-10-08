"""API mínima da Fase 00: somente registros sintéticos."""

import hmac
import os
from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Tickr PoC", docs_url=None, redoc_url=None)
origins = [
    origin.strip()
    for origin in os.getenv("POC_CORS_ORIGINS", "").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@contextmanager
def connection() -> Iterator[psycopg.Connection]:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL ausente")
    # Neon exige TLS; manter a exigência também no ambiente local.
    with psycopg.connect(
        url, connect_timeout=5, sslmode=os.getenv("POC_DB_SSLMODE", "require")
    ) as conn:
        yield conn


def authorized(authorization: str | None = Header(default=None)) -> None:
    token = os.getenv("POC_WRITE_TOKEN")
    supplied = authorization.removeprefix("Bearer ") if authorization else ""
    if not token or not hmac.compare_digest(supplied, token):
        raise HTTPException(status_code=401, detail="Não autorizado")


class SyntheticRecord(BaseModel):
    key: str = Field(min_length=1, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    value: str = Field(min_length=1, max_length=200)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "phase": "00"}


@app.get("/db")
def db_health() -> dict[str, bool]:
    try:
        with connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
            cur.fetchone()
        return {"connected": True}
    except (psycopg.Error, RuntimeError):
        raise HTTPException(status_code=503, detail="Banco indisponível") from None


@app.get("/records/{key}")
def read_record(key: str) -> dict[str, str]:
    if not 1 <= len(key) <= 80 or not all(
        ("a" <= c <= "z") or ("A" <= c <= "Z") or ("0" <= c <= "9") or c in "_-"
        for c in key
    ):
        raise HTTPException(status_code=422, detail="Chave inválida")
    try:
        with connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT value FROM poc_records WHERE key = %s", (key,))
            row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        return {"key": key, "value": row[0]}
    except HTTPException:
        raise
    except (psycopg.Error, RuntimeError):
        raise HTTPException(status_code=503, detail="Banco indisponível") from None


@app.post("/records", dependencies=[Depends(authorized)], status_code=201)
def write_record(record: SyntheticRecord) -> dict[str, str]:
    try:
        with connection() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO poc_records (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                (record.key, record.value),
            )
        return record.model_dump()
    except (psycopg.Error, RuntimeError):
        raise HTTPException(status_code=503, detail="Banco indisponível") from None


@app.post("/transaction-check", dependencies=[Depends(authorized)])
def transaction_check() -> dict[str, bool]:
    """Insere e desfaz um marcador sintético; nunca confirma a escrita."""
    try:
        with connection() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO poc_records (key, value) VALUES ('rollback_probe', 'temporary') ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value"
            )
            conn.rollback()
            cur.execute("SELECT 1 FROM poc_records WHERE key = 'rollback_probe'")
            clean = cur.fetchone() is None
        return {"rollback_ok": clean}
    except (psycopg.Error, RuntimeError):
        raise HTTPException(status_code=503, detail="Banco indisponível") from None
