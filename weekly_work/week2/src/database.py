import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "store.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_database():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS webhook_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                received_data TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )


def _utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


def store_api_data(data):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO api_logs (api_data, timestamp) VALUES (?, ?)",
            (json.dumps(data, ensure_ascii=False), _utc_timestamp()),
        )


def store_webhook_data(data):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO webhook_logs (received_data, timestamp) VALUES (?, ?)",
            (json.dumps(data, ensure_ascii=False), _utc_timestamp()),
        )
