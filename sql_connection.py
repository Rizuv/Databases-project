import sqlite3
from typing import Generator

DB_NAME = "data.db"


def init_db():
    # wywoływane raz przy starcie aplikacji — tworzy tabelę jeśli nie istnieje
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dane (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                criteria TEXT,
                mark INTEGER
            )
        """)


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # wiersze dostępne przez nazwę kolumny
    try:
        yield conn
    finally:
        conn.close()


# --- przykład użycia bez FastAPI ---
if __name__ == "__main__":
    init_db()

    for db in get_db():
        db.execute(
            "INSERT INTO dane (title, criteria, mark) VALUES (?, ?, ?)",
            ("Dune", "book", 9),
        )
        db.commit()

        cursor = db.execute("SELECT * FROM dane WHERE id = ?", (1,))
        row = cursor.fetchone()
        print(row["title"], row["mark"])  # Dune 9