# CLAUDE.md

Plik kontekstowy dla Claude. Zawiera informacje o moim stacku technologicznym, projektach i preferencjach pracy.

---

## 👤 O mnie

**Poziom umiejętności:** Prawie średniozaawansowany (powyżej początkującego)

Znam i swobodnie używam:
- OOP (klasy, konstruktory, dziedziczenie, hermetyzacja)
- Funkcje, struktury kontrolne, składnia kilku języków
- Pracę w terminalu i z bibliotekami zewnętrznymi

Aktualnie się rozwijam w kierunku poznawania nowych bibliotek oraz łączenia hardware'u z softwarem.

---

## 💻 Środowisko pracy

| Element | Wartość |
|---------|---------|
| OS | Windows 11 |
| IDE | VS Code |
| Język komunikacji | PL + EN (terminy techniczne po angielsku) |

---

## 🛠️ Stack technologiczny

### C++ — mikrokontrolery
- **Arduino** (głównie)
- **ESP32**

Zastosowania: obsługa sensorów, komunikacja przez Serial, sterowanie I/O.

### Python — software, GUI, integracje
Aktywnie używane biblioteki:
- `pyserial` — komunikacja z mikrokontrolerami
- `tkinter` — GUI
- `pygame` — GUI z animacjami / grafiką
- `numpy` — analiza i przetwarzanie danych
- `requests` — komunikacja HTTP
- `anthropic` — integracja z LLM (Claude API)

Zastosowania: software desktop, GUI z animacjami, analiza danych z mikrokontrolerów, projekty z LLM.

### MicroPython
Używam okazjonalnie do projektów, gdzie Python działa bezpośrednio na mikrokontrolerze.

### Java — mój najmocniejszy język (obecnie nieaktywny)
- **Spigot/Bukkit API** — pluginy Minecraft
- Projekty terminalowe
- Proste aplikacje GUI z JFrame

> 💡 Java to mój pierwszy język i czuję się w niej najpewniej. Porównania konceptów Python/C++ ↔ Java są dla mnie pomocne i ułatwiają zapamiętywanie.

---

## 🚧 Aktualny projekt

**Media Tracker — REST API w FastAPI**

Backend serwisu do śledzenia biblioteki mediów (książki, gry, filmy). Brak GUI, czysta logika backendowa.

**Stack:**
- `fastapi` — routing, walidacja, async
- `pydantic` — modele danych (jak Java DTOs + Bean Validation)
- `uvicorn` — ASGI server
- `sqlite3` — baza danych
- `httpx` + `pytest` — testy

**Endpoints:**
```
GET    /items          — lista (filtrowanie, sortowanie)
GET    /items/{id}     — jedna pozycja
POST   /items          — dodanie
PUT    /items/{id}     — aktualizacja
DELETE /items/{id}     — usunięcie
GET    /items/stats    — agregaty (średnia ocena, podział wg kategorii)
```

**Struktura projektu:**
```
media_tracker/
├── main.py
├── database.py
├── models.py
├── routes/items.py
├── services/item_service.py
└── repositories/item_repo.py
```

**Kluczowe koncepty do opanowania:**
- `async/await` — kooperatywna wielozadaniowość (vs Java `Thread`/`ExecutorService`)
- Pydantic — modele `ItemCreate` / `ItemResponse` / `ItemInDB`, separation of concerns w warstwie danych
- Dependency Injection przez `Depends()` — odpowiednik Spring `@Autowired`
- HTTP semantyka — status codes, idempotentność (PUT vs PATCH vs POST)
- Repository Pattern — podział na `routes/` / `services/` / `repositories/`

**Kryteria ukończenia:**
- [ ] CRUD endpoints z poprawną semantyką HTTP
- [ ] Pydantic modele z walidacją (ocena 1–10, wymagane pola)
- [ ] Persystencja w SQLite
- [ ] Separacja warstw
- [ ] Endpoint `/stats` z agregacją
- [ ] Swagger UI (`/docs`) dokumentuje wszystkie endpoints
- [ ] Min. 3 testy (GET all, POST + GET, DELETE)

---

## ⚙️ Preferencje pracy z Claude

### Język odpowiedzi
- Polski jako podstawa
- Terminy techniczne po angielsku (np. *loop*, *callback*, *thread*, *exception handling*)
- Nie tłumacz na siłę nazw bibliotek/funkcji

### Poziom wyjaśnień
- ✅ **Pomijaj** podstawy OOP, składnię, podstawowe konstrukcje
- ✅ **Wyjaśniaj** koncepty zaawansowane (np. dekoratory, metaclasses, asynchroniczność, wzorce projektowe, niskopoziomowe rzeczy w C++)
-zawsze pokazuj możliwe ulepszenia w kodzie i tłumacz mi je
- Aktywnie czytaj mój kod i wyciągaj wnisoki, proponuj odpowiednie rozwiązania na bazie moich pomyłek i pytań

### Komentarze w kodzie
- Tylko w miejscach **trudniejszych dla mnie** (nie wszędzie)
- Po polsku, ale z angielskimi pojęciami technicznymi
- Bez "oczywistych" komentarzy typu `# pętla for`

### Styl odpowiedzi
- Kod + krótkie wyjaśnienie kluczowych fragmentów
- Bez nadmiernego rozwlekania, ale bez bycia zbyt zwięzłym przy zaawansowanych tematach

### Porównania do Javy
- Tak, ale przy bardziej podstawowych koncepcjach
- Pomaga mi to budować mosty między językami i utrwalać wiedzę
- Przykłady: interfaces vs Protocols (Python), `final` vs `const`, wskaźniki w C++ vs referencje w Javie

### Sugestie rozwojowe
- ✅ Proaktywnie sugeruj ćwiczenia, podejścia, wzorce projektowe, biblioteki warte poznania
- ✅ Wskazuj gdy coś można zrobić "w bardziej profesjonalny sposób"
- ✅ Zwracaj uwagę na good practices (clean code, separation of concerns, error handling)
- Traktuj naukę jako część procesu — nie tylko "rozwiąż problem"

---

## 📋 Czego unikać

- Tłumaczenia rzeczy podstawowych (czym jest klasa, jak działa pętla)
- Komentarzy do każdej linijki kodu
- Czysto polskich tłumaczeń terminów technicznych ("wątek wykonawczy" zamiast *thread*)
- Odpowiedzi typu "to zależy" bez konkretu — preferuję konkretną rekomendację z uzasadnieniem
