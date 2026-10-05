from repositories import item_repo
import models
import sqlite3
from fastapi import HTTPException


def get_all(db: sqlite3.Connection) -> list[models.ItemResponse]:
    items = item_repo.get_all(db)
    return [models.ItemResponse(**item) for item in items]


def get_by_id(db: sqlite3.Connection, item_id: int) -> models.ItemResponse | None:
    item = item_repo.get_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=404)
    return models.ItemResponse(**item)


def create(db: sqlite3.Connection, item: models.ItemCreate) -> models.ItemResponse:
    created = item_repo.create(db, item)
    return models.ItemResponse(**created)


def delete(db: sqlite3.Connection, item_id: int) -> bool:
    return item_repo.delete(db, item_id)


def update(
    db: sqlite3.Connection, item_id: int, item: models.ItemUpdate
) -> models.ItemResponse | None:
    updated = item_repo.update(db, item_id, item)
    if updated is None:
        raise HTTPException(status_code=404)
    return models.ItemResponse(**updated)
