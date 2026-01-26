# src/services/user_service.py
from typing import List, Dict
from src.database import get_conn


def load_users() -> List[Dict]:
    """
    Pobiera wszystkich użytkowników z bazy SQLite
    i zwraca listę słowników: {"id": ..., "name": ..., "age": ...}
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, age FROM users ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    # sqlite3.Row -> zwykły dict
    return [dict(row) for row in rows]


def save_users(users: List[Dict]) -> None:
    """
    Zapisuje listę użytkowników do bazy.
    Proste podejście: czyścimy tabelę i wstawiamy wszystko od nowa.
    To jest OK przy małej liczbie rekordów (idealne na naukę).
    """
    conn = get_conn()
    cur = conn.cursor()

    # Czyścimy tabelę
    cur.execute("DELETE FROM users")

    # Wstawiamy aktualną listę
    cur.executemany(
        "INSERT INTO users (id, name, age) VALUES (?, ?, ?)",
        [(u["id"], u["name"], u["age"]) for u in users],
    )

    conn.commit()
    conn.close()
