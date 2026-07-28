import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'generic.db'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Statistic'")
if cur.fetchone() is None:
    cur.execute(
        "CREATE TABLE Statistic ("
        "id INTEGER PRIMARY KEY, "
        "display_name TEXT DEFAULT '', "
        "total_daily_claims INTEGER DEFAULT 0, "
        "total_voice_time INTEGER DEFAULT 0, "
        "total_message_send INTEGER DEFAULT 0"
        ")"
    )
    print('Created Statistic table')
else:
    cur.execute("PRAGMA table_info('Statistic')")
    columns = [row[1] for row in cur.fetchall()]
    print('existing columns', columns)
    if 'display_name' not in columns:
        cur.execute("ALTER TABLE Statistic ADD COLUMN display_name TEXT DEFAULT ''")
        print('Added display_name column')
    if 'total_message_send' not in columns:
        cur.execute("ALTER TABLE Statistic ADD COLUMN total_message_send INTEGER DEFAULT 0")
        print('Added total_message_send column')
    if 'total_voice_time' not in columns:
        cur.execute("ALTER TABLE Statistic ADD COLUMN total_voice_time INTEGER DEFAULT 0")
        print('Added total_voice_time column')
    if 'total_daily_claims' not in columns:
        cur.execute("ALTER TABLE Statistic ADD COLUMN total_daily_claims INTEGER DEFAULT 0")
        print('Added total_daily_claims column')

conn.commit()
conn.close()
print('done')
