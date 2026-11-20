import sqlite3

DB_NAME = "google_repos.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                language TEXT,
                stars INTEGER NOT NULL
            )
            """
        )


def insert_repositories(repos):
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO repositories (name, language, stars)
            VALUES (:name, :language, :stars)
            ON CONFLICT(name) DO UPDATE SET
                language = excluded.language,
                stars = excluded.stars
            """,
            repos,
        )


def select_repositories():
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, name, language, stars FROM repositories ORDER BY stars DESC, name"
        )
        return cur.fetchall()


def count_repositories():
    with get_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM repositories").fetchone()[0]
