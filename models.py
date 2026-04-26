from pydantic import BaseModel, Field
from typing import Optional


# BaseModel to klasa bazowa Pydantic — dziedzicząc po niej dostajesz automatyczną
# walidację typów, serializację do JSON i czytelny błąd gdy dane są niepoprawne.
# Odpowiednik Java DTO + Bean Validation + Jackson w jednym.


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    category: str
    rating: int = Field(ge=1, le=10)
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    title: str
    category: str
    rating: int
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=10)
    description: Optional[str] = None


if __name__ == "__main__":
    item = ItemCreate(title="Diuna", category="book", rating=9)
    print(item.title)
    print(item.description)

    # Serializacja do słownika — przydatne przy INSERT do bazy
    print(item.model_dump())
    # {"title": "Diuna", "category": "book", "rating": 9, "description": None}

    # Serializacja bez pól None — czystszy INSERT
    print(item.model_dump(exclude_none=True))
    # {"title": "Diuna", "category": "book", "rating": 9}

    # Błąd walidacji — rating poza zakresem
    try:
        bad = ItemCreate(title="Test", category="book", rating=15)
    except Exception as e:
        print(e)
        # rating: Input should be less than or equal to 10

    # ItemUpdate — tylko częściowa aktualizacja
    update = ItemUpdate(rating=10)
    print(update.model_dump(exclude_none=True))
