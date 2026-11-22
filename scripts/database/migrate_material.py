"""
將既有的 resource 資料表遷移更名為 material，完整保留既有玩家材料資料。
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
        tables = {
            row[0]
            for row in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }

        if "material" in tables and "resource" not in tables:
            print("material 資料表已完成遷移，略過。")
            return

        if "resource" not in tables:
            print("resource 資料表不存在，啟動機器人時會自動建立 material 資料表。")
            return

        if "material" in tables and "resource" in tables:
            print("同時存在 resource 與 material 資料表，請先手動確認資料後再執行遷移。")
            return

        backup_path = db_path.with_suffix(db_path.suffix + ".bak")
        shutil.copy2(db_path, backup_path)
        print(f"已備份原資料庫至：{backup_path}")

        old_count = cur.execute('SELECT COUNT(*) FROM "resource"').fetchone()[0]

        with conn:
            cur.execute('ALTER TABLE "resource" RENAME TO "material"')

        new_count = cur.execute('SELECT COUNT(*) FROM "material"').fetchone()[0]
        print(f"遷移完成！已將 resource 更名為 material，共保留 {new_count} / {old_count} 筆資料。")
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
