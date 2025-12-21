# src/database.py
import sqlite3
from pathlib import Path
import json

# Ścieżki do pliku bazy i JSON
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "users.db"
JSON_USERS = BASE_DIR / "users.json"


def get_conn() -> sqlite3.Connection:
    """
    Zwraca połączenie do bazy SQLite.
    row_factory ustawione na sqlite3.Row, żeby można było używać słownika: row["id"].
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(load_json_if_empty: bool =False) -> None:
    """
    Tworzy tabelę users (jeśli nie istnieje).
    Opcjonalnie ładuje dane z users.json, jeśli tabela jest pusta.
    """
    print("INIT DB START")

    conn = get_conn()
    cursor = conn.cursor()

    # Tworzenie tabeli
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age  INTEGER NOT NULL
        )
        """
    )
    conn.commit()

    if load_json_if_empty:
        # Sprawdź, czy tabela jest pusta
        cursor.execute("SELECT COUNT(*) AS cnt FROM users")
        count = cursor.fetchone()["cnt"]

        # Jeśli pusta i istnieje users.json → załaduj
        if count == 0 and JSON_USERS.exists():
            with open(JSON_USERS, "r", encoding="utf-8") as f:
                users = json.load(f)

            for u in users:
                cursor.execute(
                    "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
                    (u["id"], u["name"], u["age"]),
                )

            conn.commit()

    conn.close()
    
# --- SQL OPERATIONS ---

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, age FROM users")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

def get_user_by_id(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()

    conn.close()
    return dict(row) if row else None

def add_user(name: str, age: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)",
        (name, age)
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_user(user_id: int, name: str, age: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name = ?, age = ? WHERE id = ?",
        (name, age, user_id)
    )

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated > 0


def delete_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    deleted = cursor.rowcount
    conn.close()

    return deleted > 0

def query_users(limit, offset, sort_column, 
    sort,direction, 
    min_age=None, max_age=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    base_query = "SELECT * FROM users"
    conditions = []
    params = []
      
    if min_age is not None:
       conditions.append("age >= {min_age}")
       params.append(min_age)
       
    if max_age is not None:
       conditions.append("age <= ?")
       params.append(max_age)
            
    if conditions:
       base_query += " WHERE " + " AND ".join(conditions)
       
       #KLUCZOWE: spacje + whitelist kolumn
       allowed_columns = {"id", "name", "age"}
       if sort_column not in allowed_columns:
           sort_column = "id"
           
           sort_direction = " DESC" if sort_direction == "DESC" else "ASC"
           
           base_query += f" ORDER BY {sort_column} {sort_direction}"
           base_query += " LIMIT ? OFFSET ?"
           
           params.extend([limit, offset])
           
           cursor.execute(base_query,params)
           rows = cursor.fetchall()
           return [dict(row) for row in rows]                  
    