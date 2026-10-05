import sqlite3
from typing import Generator

DB_NAME = "data.db"


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dane (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT,
                description TEXT
            )
        """)


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
