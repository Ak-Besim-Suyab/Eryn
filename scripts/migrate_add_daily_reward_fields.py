import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "database" / "generic.db"


def column_exists(cursor: sqlite3.Cursor, table: str, column: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cursor.fetchall())


def add_column(cursor: sqlite3.Cursor, table: str, ddl: str) -> None:
    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {ddl};")


def main() -> None:
    db_path = get_db_path()
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        table = "player"

        if not column_exists(cursor, table, "daily_reward"):
            add_column(cursor, table, "daily_reward INTEGER NOT NULL DEFAULT 1")

        if not column_exists(cursor, table, "daily_reward_timestamp"):
            add_column(cursor, table, "daily_reward_timestamp DATETIME")

        conn.commit()

    print("Migration complete.")


if __name__ == "__main__":
    main()
