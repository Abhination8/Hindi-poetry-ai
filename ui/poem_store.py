import sqlite3
from datetime import datetime

DB_PATH = "ui/poems.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS poems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        theme TEXT,
        mood TEXT,
        style TEXT,
        meter TEXT,
        poets TEXT,
        created_at TEXT,
        rating INTEGER
    )
    """)

    conn.commit()
    conn.close()


def save_poem(text, theme, mood, style, meter, poets):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO poems (text, theme, mood, style, meter, poets, created_at, rating)
    VALUES (?, ?, ?, ?, ?, ?, ?, NULL)
    """, (
        text,
        theme,
        mood,
        style,
        meter,
        ",".join(poets),
        datetime.utcnow().isoformat()
    ))

    poem_id = cur.lastrowid
    conn.commit()
    conn.close()
    return poem_id


def update_rating(poem_id, rating):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "UPDATE poems SET rating = ? WHERE id = ?",
        (rating, poem_id)
    )

    conn.commit()
    conn.close()


def get_liked_poems(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT text FROM poems
    WHERE rating = 1
    ORDER BY created_at DESC
    LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]