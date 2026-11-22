"""
將既有的 statistic 資料表遷移為透過 player_id 外鍵關聯 player(id) 的結構，
完整保留原本的 total_daily / total_voice / total_message 統計資料。
"""
import shutil
import sqlite3
from pathlib import Path

from config import DATABASE_PATH


def migrate():
    db_path = Path(DATABASE_PATH)
    if not db_path.exists():
        print(f"找不到資料庫檔案：{db_path}")
        return

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        columns = [row[1] for row in cur.execute("PRAGMA table_info(statistic)").fetchall()]

        if not columns:
            print("statistic 資料表尚未建立，啟動機器人時會自動以新結構建立。")
            return

        if "player_id" in columns:
            print("statistic 資料表已完成遷移（已有 player_id 欄位），略過。")
            return

        backup_path = db_path.with_suffix(db_path.suffix + ".bak")
        shutil.copy2(db_path, backup_path)
        print(f"已備份原資料庫至：{backup_path}")

        old_count = cur.execute("SELECT COUNT(*) FROM statistic").fetchone()[0]

        with conn:
            # 確保每筆統計資料的 id 都有對應的 player 紀錄
            cur.execute("""
                INSERT OR IGNORE INTO player (id)
                SELECT id FROM statistic
            """)

            cur.execute("""
                CREATE TABLE "statistic_new" (
                    "id" INTEGER NOT NULL PRIMARY KEY,
                    "player_id" INTEGER NOT NULL,
                    "total_daily" INTEGER NOT NULL DEFAULT 0,
                    "total_voice" INTEGER NOT NULL DEFAULT 0,
                    "total_message" INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY ("player_id") REFERENCES "player" ("id") ON DELETE CASCADE
                )
            """)

            cur.execute("""
                INSERT INTO "statistic_new" ("player_id", "total_daily", "total_voice", "total_message")
                SELECT
                    "id",
                    COALESCE("total_daily", 0),
                    COALESCE(CAST("total_voice" AS INTEGER), 0),
                    COALESCE("total_message", 0)
                FROM "statistic"
            """)

            cur.execute('DROP TABLE "statistic"')
            cur.execute('ALTER TABLE "statistic_new" RENAME TO "statistic"')
            cur.execute('CREATE UNIQUE INDEX "statistic_player_id" ON "statistic" ("player_id")')

        new_count = cur.execute("SELECT COUNT(*) FROM statistic").fetchone()[0]
        print(f"遷移完成！共保留 {new_count} / {old_count} 筆統計資料。")
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
