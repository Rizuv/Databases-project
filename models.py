from pydantic import BaseModel, Field
from typing import Optional


# BaseModel to klasa bazowa Pydantic — dziedzicząc po niej dostajesz automatyczną
# walidację typów, serializację do JSON i czytelny błąd gdy dane są niepoprawne.
# Odpowiednik Java DTO + Bean Validation + Jackson w jednym.


class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    category: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    title: str
    category: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[str] = None
    description: Optional[str] = None


if __name__ == "__main__":
    pass
