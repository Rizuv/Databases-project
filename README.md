Aplikacja pozwala dodawać, przeglądać, edytować i usuwać pozycje z biblioteki. Każda pozycja ma tytuł, kategorię i opis.
Dane są przechowywane w SQLite, a walidację wejścia i wyjścia zapewnia Pydantic.
Kod jest podzielony na cztery warstwy, tak aby każda odpowiadała za jedną rzecz: trasy (routes) obsługują tylko HTTP, serwisy (services) zawierają obsługę błędów 404, repozytoria (repositories) wykonują zapytania SQL, a sql_connection.py zarządza połączeniem z bazą.
Połączenie jest tworzone osobno dla każdego requestu i wstrzykiwane przez Depends().
Zapytania SQL używają parametrów (?),
dzięki czemu kod jest odporny na SQL injection
