import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


DATABASE_PATH = Path(
    os.environ.get("TODO_DATABASE_PATH", Path(__file__).with_name("todos.db"))
)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute("PRAGMA journal_mode = WAL")
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                grade INTEGER CHECK (grade BETWEEN 1 AND 12),
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
                completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1)),
                created_at TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high')),
                due_date TEXT,
                category TEXT NOT NULL DEFAULT 'General' CHECK (length(category) BETWEEN 1 AND 50)
            );

            CREATE INDEX IF NOT EXISTS idx_todos_user_created
                ON todos(user_id, created_at DESC, id DESC);

            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                expires_at INTEGER NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_expiry ON sessions(expires_at);

            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL COLLATE NOCASE,
                attempted_at INTEGER NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_login_attempts_email_time
                ON login_attempts(email, attempted_at);

            CREATE TABLE IF NOT EXISTS study_tips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                tip TEXT NOT NULL,
                normalized_tip TEXT NOT NULL,
                subject TEXT NOT NULL DEFAULT 'General',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, normalized_tip)
            );

            CREATE INDEX IF NOT EXISTS idx_study_tips_user_created
                ON study_tips(user_id, id DESC);

            CREATE TABLE IF NOT EXISTS user_subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                subject TEXT NOT NULL,
                UNIQUE (user_id, subject)
            );

            CREATE INDEX IF NOT EXISTS idx_user_subjects_user
                ON user_subjects(user_id);

            CREATE TABLE IF NOT EXISTS pyqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_grade INTEGER NOT NULL CHECK (class_grade BETWEEN 1 AND 12),
                subject TEXT NOT NULL,
                chapter TEXT NOT NULL,
                year INTEGER NOT NULL,
                exam_type TEXT NOT NULL DEFAULT 'Board/Annual Exam',
                marks INTEGER NOT NULL DEFAULT 3,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_pyqs_class_sub
                ON pyqs(class_grade, subject, year);

            CREATE TABLE IF NOT EXISTS generated_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                class_grade INTEGER NOT NULL,
                subject TEXT NOT NULL,
                chapter TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_generated_notes_user
                ON generated_notes(user_id, id DESC);
            """
        )
        user_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(users)")
        }
        if "grade" not in user_columns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN grade INTEGER "
                "CHECK (grade BETWEEN 1 AND 12)"
            )
        if "language" not in user_columns:
            connection.execute(
                "ALTER TABLE users ADD COLUMN language TEXT NOT NULL DEFAULT 'en'"
            )

        todo_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(todos)")
        }
        if "priority" not in todo_columns:
            connection.execute(
                "ALTER TABLE todos ADD COLUMN priority TEXT NOT NULL DEFAULT 'medium'"
            )
        if "due_date" not in todo_columns:
            connection.execute(
                "ALTER TABLE todos ADD COLUMN due_date TEXT"
            )
        if "category" not in todo_columns:
            connection.execute(
                "ALTER TABLE todos ADD COLUMN category TEXT NOT NULL DEFAULT 'General'"
            )

        tip_columns = {
            row["name"] for row in connection.execute("PRAGMA table_info(study_tips)")
        }
        if "subject" not in tip_columns:
            connection.execute(
                "ALTER TABLE study_tips ADD COLUMN subject TEXT NOT NULL DEFAULT 'General'"
            )

        # Seed initial PYQs if table is empty
        pyq_count = connection.execute("SELECT COUNT(*) AS total FROM pyqs").fetchone()["total"]
        if pyq_count == 0:
            from app.ncert_data import INITIAL_PYQS
            for item in INITIAL_PYQS:
                connection.execute(
                    """
                    INSERT INTO pyqs (class_grade, subject, chapter, year, exam_type, marks, question, answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item["class_grade"],
                        item["subject"],
                        item["chapter"],
                        item["year"],
                        item["exam_type"],
                        item["marks"],
                        item["question"],
                        item["answer"],
                    ),
                )


