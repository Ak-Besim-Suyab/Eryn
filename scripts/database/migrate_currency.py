"""
將 player 資料表的 currency 欄位以加法合併至 currency 資料表對應 player_id 的 vin 欄位，
合併完成後刪除 player 資料表的 currency 欄位。
"""
import sqlite3
from pathlib import Path

from config import DATABASE_PATH


def migrate(db_path: Path | str = DATABASE_PATH):
    db_path = Path(db_path)
    if not db_path.exists():
        print(f"找不到資料庫檔案：{db_path}")
        return

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        player_cols = [row[1] for row in cur.execute('PRAGMA table_info("player")').fetchall()]

        if "currency" not in player_cols:
            print("player 資料表已沒有 currency 欄位（可能已完成遷移），略過。")
            return

        # 檢查是否存在同 id 卻有不同 currency 數值的異常重複列
        conflicts = cur.execute("""
            SELECT "id", MIN("currency"), MAX("currency")
            FROM "player"
            WHERE "id" IS NOT NULL AND "currency" IS NOT NULL
            GROUP BY "id"
            HAVING MIN("currency") != MAX("currency")
        """).fetchall()
        if conflicts:
            raise RuntimeError(f"發現同 id 有不同 currency 數值的重複列：{conflicts}")

        # player.id 未設 PRIMARY KEY，可能含重複列，先依 id 去重取唯一非 NULL 的 currency
        before_player_count, before_player_sum = cur.execute("""
            SELECT COUNT(*), COALESCE(SUM(val), 0)
            FROM (
                SELECT "id", MAX("currency") AS val
                FROM "player"
                WHERE "id" IS NOT NULL
                GROUP BY "id"
                HAVING val IS NOT NULL AND val != 0
            )
        """).fetchone()
        before_vin_sum = cur.execute(
            'SELECT COALESCE(SUM("vin"), 0) FROM "currency"'
        ).fetchone()[0]

        with conn:
            cur.execute("""
                INSERT INTO "currency" ("player_id", "vin")
                SELECT "id", MAX("currency") AS val
                FROM "player"
                WHERE "id" IS NOT NULL
                GROUP BY "id"
                HAVING val IS NOT NULL AND val != 0
                ON CONFLICT("player_id") DO UPDATE SET
                    "vin" = "currency"."vin" + excluded."vin"
            """)

            cur.execute('ALTER TABLE "player" DROP COLUMN "currency"')

        after_vin_count, after_vin_sum = cur.execute(
            'SELECT COUNT(*), COALESCE(SUM("vin"), 0) FROM "currency"'
        ).fetchone()

        expected_sum = before_vin_sum + before_player_sum
        if after_vin_sum != expected_sum:
            raise RuntimeError(f"總和驗證失敗：預期 {expected_sum}，實際 {after_vin_sum}")

        print(f"已合併 {before_player_count} 筆 player.currency（總計 {before_player_sum:,}）至 currency.vin")
        print(f"currency.vin 總和：{before_vin_sum:,} -> {after_vin_sum:,}（共 {after_vin_count} 筆紀錄）")
        print("已成功刪除 player 資料表的 currency 欄位。")
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
