import argparse
import sqlite3
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "generic.db"

EXPECTED_COLUMNS = {
    "id": "INTEGER",
    "display_name": "TEXT",
    "total_daily_claims": "INTEGER",
    "total_voice_time": "INTEGER",
    "total_message_send": "INTEGER",
}


def connect_db():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")
    return sqlite3.connect(DB_PATH)


def get_table_info(conn, table_name: str):
    cursor = conn.execute(f"PRAGMA table_info('{table_name}')")
    rows = cursor.fetchall()
    return [
        {
            "cid": row[0],
            "name": row[1],
            "type": row[2],
            "notnull": bool(row[3]),
            "default_value": row[4],
            "pk": bool(row[5]),
        }
        for row in rows
    ]


def has_table(conn, table_name: str) -> bool:
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def inspect_statistic_table(conn):
    if not has_table(conn, "Statistic"):
        print("Statistic table does not exist.")
        return

    info = get_table_info(conn, "Statistic")
    print("Statistic table columns:")
    for column in info:
        print(
            f"  - {column['name']} {column['type']} pk={column['pk']} notnull={column['notnull']} default={column['default_value']}"
        )

    keys = {col["name"] for col in info}
    if "id" in keys and "display_name" in keys:
        print("Current Statistic schema appears to be the new independent format.")
    elif "player_id" in keys or "player" in keys:
        print("Current Statistic schema appears to be the old bound format.")
    else:
        print("Current Statistic schema is not recognized by this migration script.")


def create_statistic_table(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS Statistic ("
        "id INTEGER PRIMARY KEY, "
        "display_name TEXT DEFAULT '', "
        "total_daily_claims INTEGER DEFAULT 0, "
        "total_voice_time INTEGER DEFAULT 0, "
        "total_message_send INTEGER DEFAULT 0"
        ")"
    )
    conn.commit()
    print("Created independent Statistic table.")


def migrate_statistic_table(conn):
    if not has_table(conn, "Statistic"):
        print("Statistic table does not exist. Creating independent Statistic table.")
        create_statistic_table(conn)
        return

    info = get_table_info(conn, "Statistic")
    current_columns = {col["name"] for col in info}

    if "id" in current_columns and "display_name" in current_columns:
        print("Statistic table already uses the new schema; no migration needed.")
        return

    if "player_id" in current_columns:
        source_key = "player_id"
    elif "player" in current_columns:
        source_key = "player"
    else:
        raise RuntimeError(
            "Cannot determine source player key column in Statistic table."
        )

    print(f"Migrating Statistic table from '{source_key}' to independent 'id' schema...")

    conn.execute("PRAGMA foreign_keys = OFF")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_table = f"Statistic_backup_{timestamp}"

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Statistic_new ("
        "id INTEGER PRIMARY KEY, "
        "display_name TEXT DEFAULT '', "
        "total_daily_claims INTEGER DEFAULT 0, "
        "total_voice_time INTEGER DEFAULT 0, "
        "total_message_send INTEGER DEFAULT 0"
        ")"
    )

    if has_table(conn, "Player"):
        cursor.execute(
            f"INSERT INTO Statistic_new (id, display_name, total_daily_claims, total_voice_time, total_message_send) "
            f"SELECT old.{source_key} AS id, COALESCE(p.display_name, '') AS display_name, "
            f"COALESCE(old.total_daily_claims, 0), COALESCE(old.total_voice_time, 0), "
            f"COALESCE(old.total_message_send, 0) "
            f"FROM Statistic AS old LEFT JOIN Player AS p ON p.id = old.{source_key}"
        )
    else:
        cursor.execute(
            f"INSERT INTO Statistic_new (id, total_daily_claims, total_voice_time, total_message_send) "
            f"SELECT old.{source_key} AS id, COALESCE(old.total_daily_claims, 0), "
            f"COALESCE(old.total_voice_time, 0), COALESCE(old.total_message_send, 0) "
            f"FROM Statistic AS old"
        )

    cursor.execute(f"ALTER TABLE Statistic RENAME TO {backup_table}")
    cursor.execute("ALTER TABLE Statistic_new RENAME TO Statistic")

    conn.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    print("Migration completed.")
    print(f"Original Statistic table retained as '{backup_table}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Inspect and migrate the Statistic database schema for independence from Player.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Inspect the existing Statistic schema without making changes.",
    )
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Migrate the Statistic table to the new independent schema.",
    )
    args = parser.parse_args()

    if not args.check and not args.migrate:
        parser.error("At least one of --check or --migrate is required.")

    conn = connect_db()
    try:
        if args.check:
            inspect_statistic_table(conn)
        if args.migrate:
            migrate_statistic_table(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
