# Notatki — Media Tracker, sesja 1

## Co zbudowaliśmy

Szkielet projektu REST API w FastAPI:
- `main.py` — punkt wejścia, serwer FastAPI
- `models.py` — modele Pydantic (walidacja danych)
- `sql_connection.py` — połączenie z SQLite, wzorzec connection-per-request
- `structure.md` — architektura projektu i kolejność implementacji

---

## 1. SQLite — podstawy

```python
cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
row = cursor.fetchone()   # jeden wiersz lub None
rows = cursor.fetchall()  # lista wierszy
```

**Zawsze używaj `?` jako placeholder** — nigdy f-stringa. F-string to SQL injection.

**`row_factory`** — zamiast tupli `(1, "Diuna", 9)` dostajesz dostęp po nazwie:
```python
conn.row_factory = sqlite3.Row
row["title"]   # zamiast row[1]
```

**AUTOINCREMENT** — SQLite nadaje `id` samo, nie zarządzaj nim ręcznie:
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```
W INSERT pomijasz `id`:
```python
cursor.execute("INSERT INTO items (title, rating) VALUES (?, ?)", (title, rating))
```

---

## 2. Generator i `yield`

Zwykła funkcja zwraca raz i "znika". Funkcja z `yield` to **generator** — zatrzymuje się i czeka:

```python
def get_db():
    conn = sqlite3.connect("data.db")
    try:
        yield conn        # zatrzymanie — oddaj conn wywołującemu
    finally:
        conn.close()      # wykona się gdy generator zostanie zamknięty
```

Przepływ:
1. `next(generator)` — wykonuje do `yield`, oddaje `conn`
2. Wywołujący używa `conn`
3. `generator.close()` — wznawia od `yield`, wchodzi do `finally`, zamyka połączenie

---

## 3. `finally` — gwarancja sprzątania

```python
try:
    conn = sqlite3.connect("data.db")
    yield conn
    # tutaj może być wyjątek
finally:
    conn.close()   # wykona się ZAWSZE — nawet gdy był wyjątek
```

Bez `finally` — przy wyjątku `conn.close()` nigdy by się nie wykonało (resource leak).

Java odpowiednik: `try-with-resources` z `AutoCloseable`.

---

## 4. `with` — skrócony `try/finally`

`with` działa na obiektach które mają `__enter__` i `__exit__` (context manager protocol):

```python
with sqlite3.connect("data.db") as conn:
    conn.execute("INSERT ...")
# tutaj: automatyczny commit + zamknięcie połączenia
```

Równoważne z:
```python
conn = sqlite3.connect("data.db")
try:
    conn.execute("INSERT ...")
    conn.commit()
finally:
    conn.close()
```

---

## 5. Connection-per-request — dlaczego ważne

**Złe podejście** — jedno połączenie na cały czas życia aplikacji:
```python
class DB:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")  # dzielone między wszystkie requesty
```
Problem: SQLite nie obsługuje równoległych zapisów przez jedno połączenie → `OperationalError: database is locked`.

**Dobre podejście** — nowe połączenie na każdy request, zamykane po zakończeniu:
```python
def get_db():
    conn = sqlite3.connect("data.db")
    try:
        yield conn
    finally:
        conn.close()
```

W FastAPI wstrzykujesz przez `Depends()` — framework wywołuje generator automatycznie.

---

## 6. FastAPI — podstawy

**Rejestrowanie endpointów przez dekoratory:**
```python
app = FastAPI()

@app.get("/items")        # GET /items
def list_items():
    return [{"id": 1}]    # dict/lista → automatycznie serializowane do JSON
```

**Skąd FastAPI bierze dane** — patrzy na nazwy i typy parametrów:
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):          # z URL path — /items/5 → item_id=5

@app.get("/items")
def list_items(category: str = None): # z query string — /items?category=book

@app.post("/items")
def create_item(item: ItemCreate):    # z request body (JSON) — Pydantic model
```

**Uruchamianie:**
```bash
uvicorn main:app --reload
# main = plik main.py, app = obiekt FastAPI, --reload = auto-restart po zmianach
```

Swagger UI automatycznie pod `localhost:8000/docs`.

---

## 7. Pydantic — `BaseModel` i `Field`

`BaseModel` = Java DTO + Bean Validation + Jackson w jednym.

```python
from pydantic import BaseModel, Field
from typing import Optional

class ItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    category: str                          # wymagane, tylko typ
    rating: int = Field(ge=1, le=10)       # ge = >=, le = <=
    description: Optional[str] = None      # niewymagane, domyślnie None
```

**Walidacja działa automatycznie:**
```python
item = ItemCreate(title="Diuna", category="book", rating=15)
# ValidationError — rating musi być <= 10
# FastAPI zwraca 422 Unprocessable Entity zanim Twój kod w ogóle się wykona
```

**Serializacja:**
```python
item.model_dump()                    # → dict ze wszystkimi polami
item.model_dump(exclude_none=True)   # → dict bez pól None
item.model_dump_json()               # → string JSON
```

**Parametry `Field()`:**
| Parametr | Znaczenie |
|---|---|
| `ge` | >= (greater or equal) |
| `le` | <= (less or equal) |
| `gt` | > (greater than) |
| `lt` | < (less than) |
| `min_length` | minimalna długość stringa |
| `max_length` | maksymalna długość stringa |
| `default` | wartość domyślna |

---

## 8. Trzy modele — wzorzec

```python
class ItemCreate(BaseModel):   # wchodzi przy POST — bez id
    title: str
    rating: int = Field(ge=1, le=10)

class ItemResponse(BaseModel): # wychodzi z API — z id
    id: int
    title: str
    rating: int

class ItemUpdate(BaseModel):   # wchodzi przy PUT — wszystko Optional
    title: Optional[str] = None
    rating: Optional[int] = Field(default=None, ge=1, le=10)
```

Jeden model na wszystko to częsty błąd — `id` nie istnieje przy tworzeniu, ale musi być w response. Rozdzielenie modeli wymusza to na poziomie typów.

---

## 9. Architektura projektu

```
routes/items.py           ← tylko HTTP: parsowanie requestu, status codes
    ↓
services/item_service.py  ← logika biznesowa: walidacja, reguły, kalkulacje
    ↓
repositories/item_repo.py ← tylko SQL: zapytania, nic więcej
    ↓
database.py               ← połączenie SQLite
```

Odpowiednik Spigot: `PlayerDataManager`, `ConfigManager` = Repository Pattern.
Odpowiednik Spring: `@Controller` → `@Service` → `@Repository`.

**`Depends()` — wstrzykiwanie połączenia:**
```python
@router.get("/items")
def list_items(db: sqlite3.Connection = Depends(get_db)):
    # db = świeże połączenie tylko dla tego requestu
    # po zakończeniu handlera → finally → conn.close()
```

---

## Co dalej (następna sesja)

1. `database.py` — `init_db()` + finalna wersja `get_db()`
2. `repositories/item_repo.py` — zapytania SQL
3. `services/item_service.py` — logika + obsługa 404
4. `routes/items.py` — wszystkie endpointy CRUD
5. Podpięcie routera w `main.py`
6. Endpoint `/stats` + testy
