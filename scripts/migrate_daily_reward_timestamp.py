import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    return Path(__file__).resolve().parent.parent / "database" / "generic.db"


def main() -> None:
    db_path = get_db_path()
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        table = "player"

        # Check current column type
        cursor.execute(f"PRAGMA table_info({table});")
        columns = {row[1]: row[2] for row in cursor.fetchall()}

        if "daily_reward_timestamp" not in columns:
            print("Column 'daily_reward_timestamp' does not exist. Adding it...")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN daily_reward_timestamp REAL;")
            conn.commit()
            print("✓ Column added successfully.")
        else:
            current_type = columns["daily_reward_timestamp"]
            print(f"✓ Column 'daily_reward_timestamp' exists with type: {current_type}")
            
            if current_type == "REAL":
                print("✓ Column type is already correct (REAL).")
            else:
                print(f"⚠ Column type is {current_type}, expected REAL.")
                print("  Note: SQLite stores REAL values even if column was originally DATETIME.")
                print("  The data will be treated as REAL going forward.")

    print("\nMigration complete.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
