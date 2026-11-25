"""
移除 player 資料表中已遷移至 attribute 資料表的 san、luck、karma 欄位。
（目前所有玩家的這三個欄位皆維持預設值未曾更動，因此直接移除。）
"""
import sqlite3
from pathlib import Path

from config import DATABASE_PATH

TARGET_COLUMNS = ("san", "luck", "karma")


def migrate(db_path: Path | str = DATABASE_PATH):
    db_path = Path(db_path)
    if not db_path.exists():
        print(f"找不到資料庫檔案：{db_path}")
        return

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        player_cols = {
            row[1] for row in cur.execute('PRAGMA table_info("player")').fetchall()
        }
        cols_to_drop = [col for col in TARGET_COLUMNS if col in player_cols]

        if not cols_to_drop:
            print("player 資料表已沒有 san、luck、karma 欄位（可能已完成遷移），略過。")
            return

        with conn:
            for col in cols_to_drop:
                cur.execute(f'ALTER TABLE "player" DROP COLUMN "{col}"')

        print(f"已成功從 player 資料表移除欄位：{', '.join(cols_to_drop)}")
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
