import sqlite3
import models


def get_all(db: sqlite3.Connection) -> list[dict]:
    rows = db.execute("SELECT * FROM dane").fetchall()
    return [dict(row) for row in rows]


def get_by_id(db: sqlite3.Connection, item_id: int) -> dict | None:
    data = db.execute("SELECT * FROM dane WHERE id = ?", (item_id,)).fetchone()
    if data is None:
        return None
    else:
        return dict(data)


def create(db: sqlite3.Connection, item: models.ItemCreate) -> dict:
    data = item.model_dump()
    row = db.execute(
        "INSERT INTO dane (title, category, description) VALUES (?, ?, ?)",
        (data["title"], data["category"], data["description"]),
    )
    db.commit()  # wazne, zeby zapisac zmiane
    return get_by_id(db, row.lastrowid)


def delete(db: sqlite3.Connection, item_id: int) -> bool:
    cursor = db.execute("DELETE FROM dane WHERE id = ?", (item_id,))
    db.commit()
    is_deleted = cursor.rowcount
    # return True if is_deleted == 1 else False ---> też dobrze
    return is_deleted == 1


def update(
    db: sqlite3.Connection, item_id: int, item: models.ItemUpdate
) -> dict | None:
    # tylko pola które faktycznie przyszły w request body (reszta to None)
    dane = item.model_dump(exclude_none=True)

    # "title = ?, category = ?" — dynamicznie, zależnie od tego co przyszło
    fields = ", ".join(f"{key} = ?" for key in dane)

    # wartości dla SET + item_id dla WHERE id = ? (musi być na końcu)
    values = list(dane.values()) + [item_id]

    db.execute(
        f"UPDATE dane SET {fields} WHERE id = ?",  # f-string bezpieczny — klucze pochodzą z modelu Pydantic, nie od użytkownika
        values,
    )
    db.commit()
    return get_by_id(db, item_id)
