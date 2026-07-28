import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "generic.db"


def migrate_statistic_player_id_to_id(db_path: Path = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Statistic'")
    if cur.fetchone() is None:
        raise FileNotFoundError(f"Statistic table not found in {db_path}")

    cur.execute("PRAGMA table_info('Statistic')")
    columns = [row[1] for row in cur.fetchall()]

    if "player_id" not in columns:
        print("No player_id column found; nothing to migrate.")
        conn.close()
        return

    if "id" not in columns:
        cur.execute("ALTER TABLE Statistic ADD COLUMN id INTEGER")

    cur.execute("SELECT COUNT(*) FROM Statistic WHERE player_id IS NOT NULL")
    count = cur.fetchone()[0]
    print(f"Migrating {count} rows from player_id to id...")

    cur.execute("UPDATE Statistic SET id = player_id WHERE id IS NULL OR id = 0")
    cur.execute("ALTER TABLE Statistic DROP COLUMN player_id")
    conn.commit()

    print("Migration completed successfully.")
    conn.close()


if __name__ == "__main__":
    migrate_statistic_player_id_to_id()
