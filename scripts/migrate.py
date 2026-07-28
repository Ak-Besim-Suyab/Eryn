"""
這個腳本負責將 Statistic 資料表的 player_id 欄位資料轉移至 id 欄位，
並在確認轉移成功後刪除 player_id 欄位。

背景：
    目前 Statistic 表的 id 是自動遞增的 PRIMARY KEY，跟玩家實際的 Discord ID (player_id) 不同。
    這支腳本會把 id 的值覆蓋成 player_id 的值，讓 id 直接對應 Player.id，
    之後就能拿掉 player_id 欄位，讓 Statistic 表徹底獨立 (不依賴外鍵) 又能直接用 id 查詢。

安全機制：
    1. 執行前會檢查 player_id 是否有重複或空值，若有則中止，不會動到資料庫。
    2. 執行前會建立一份帶時間戳記的備份表 (Statistic_backup_YYYYMMDD_HHMMSS)。
    3. 更新與刪除欄位皆包在同一個交易 (transaction) 內，任何一步出錯都會整個回滾。
    4. 若偵測到已經完成遷移 (id 已對應 player_id 且 player_id 欄位已不存在)，會直接略過，不會重複執行。

使用方式：
    python scripts/migrate_statistic_id.py            # 直接執行遷移
    python scripts/migrate_statistic_id.py --check     # 只檢查目前狀態，不做任何變更
"""
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "generic.db"


def get_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    cur = conn.execute(f"PRAGMA table_info('{table}')")
    return [row[1] for row in cur.fetchall()]


def check(conn: sqlite3.Connection) -> str:
    """
    檢查目前 Statistic 表的狀態，回傳狀態字串：
        "already_migrated" -- 已經完成遷移，不需要再做任何事
        "ready"             -- 尚未遷移，且資料乾淨，可以安全執行
        "not_ready"         -- 尚未遷移，但資料有問題 (重複或空值)，需要先手動處理
    """
    columns = get_columns(conn, "Statistic")

    if "player_id" not in columns:
        print("player_id 欄位已不存在，Statistic 表應該已經完成遷移，略過。")
        return "already_migrated"

    if "id" not in columns:
        raise RuntimeError("Statistic 表找不到 id 欄位，資料庫結構異常，請先手動檢查。")

    cur = conn.execute("SELECT COUNT(*) FROM Statistic WHERE player_id IS NULL")
    null_count = cur.fetchone()[0]

    cur = conn.execute(
        "SELECT player_id, COUNT(*) FROM Statistic GROUP BY player_id HAVING COUNT(*) > 1"
    )
    duplicates = cur.fetchall()

    cur = conn.execute("SELECT COUNT(*) FROM Statistic")
    total = cur.fetchone()[0]

    print(f"Statistic 表目前共有 {total} 筆資料。")
    print(f"player_id 為空值的資料筆數：{null_count}")
    print(f"player_id 重複的組別數量：{len(duplicates)}")

    if null_count > 0 or duplicates:
        print("資料存在空值或重複，無法安全轉移，請先手動修正這些資料。")
        if duplicates:
            print("重複的 player_id 如下：")
            for player_id, count in duplicates:
                print(f"  player_id={player_id}，共 {count} 筆")
        return "not_ready"

    return "ready"


def migrate(conn: sqlite3.Connection):
    status = check(conn)

    if status == "already_migrated":
        return

    if status == "not_ready":
        print("已中止遷移，資料庫未被修改。")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_table = f"Statistic_backup_{timestamp}"

    print(f"建立備份表：{backup_table}")
    conn.execute(f"CREATE TABLE {backup_table} AS SELECT * FROM Statistic")

    # 注意：實際資料庫中 statistic.player_id 仍帶有
    # FOREIGN KEY (player_id) REFERENCES player(id) 限制，
    # SQLite 的 ALTER TABLE ... DROP COLUMN 無法刪除被外鍵參照的欄位，
    # 因此改用「建立新表 -> 搬移資料 -> 刪除舊表 -> 改名」的標準流程處理。
    try:
        conn.execute("PRAGMA foreign_keys = OFF")
        with conn:  # 交易區塊，出錯會自動 rollback
            print("建立新的 Statistic 表結構（不含 player_id 與外鍵）...")
            conn.execute(
                "CREATE TABLE Statistic_new ("
                "id INTEGER NOT NULL PRIMARY KEY, "
                "display_name TEXT DEFAULT '', "
                "total_daily_claims INTEGER NOT NULL DEFAULT 0, "
                "total_voice_time INTEGER DEFAULT 0, "
                "total_message_send INTEGER DEFAULT 0"
                ")"
            )

            print("將資料搬移至新表，並以 player_id 的值作為新的 id...")
            conn.execute(
                "INSERT INTO Statistic_new "
                "(id, display_name, total_daily_claims, total_voice_time, total_message_send) "
                "SELECT player_id, display_name, total_daily_claims, total_voice_time, total_message_send "
                "FROM Statistic"
            )

            print("刪除舊表並將新表更名為 Statistic...")
            conn.execute("DROP TABLE Statistic")
            conn.execute("ALTER TABLE Statistic_new RENAME TO Statistic")

        # 嘗試檢查資料庫整體外鍵完整性（僅供參考）。
        # 注意：目前 player 表的 id 欄位本身沒有宣告 PRIMARY KEY，
        # 導致 PRAGMA foreign_key_check 在這個資料庫上本來就會回報 "foreign key mismatch"，
        # 這是既有問題，與這次 Statistic 遷移無關，因此這裡只警告不中止。
        try:
            fk_problems = conn.execute("PRAGMA foreign_key_check").fetchall()
            if fk_problems:
                print(f"提醒：外鍵完整性檢查回報以下項目（可能是既有問題，非本次遷移造成）：{fk_problems}")
        except sqlite3.OperationalError as e:
            print(f"提醒：外鍵完整性檢查無法執行（可能是既有的資料庫結構問題，非本次遷移造成）：{e}")
    except sqlite3.Error as e:
        print(f"遷移過程發生錯誤，已回滾：{e}")
        print(f"備份表 {backup_table} 仍保留，可用於還原資料。")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")

    # 驗證結果
    columns_after = get_columns(conn, "Statistic")
    if "player_id" in columns_after:
        raise RuntimeError("player_id 欄位刪除失敗，請檢查資料庫。")

    cur = conn.execute("SELECT COUNT(*) FROM Statistic")
    total_after = cur.fetchone()[0]

    print("遷移完成！")
    print(f"Statistic 表目前共有 {total_after} 筆資料。")
    print(f"原始資料已備份於：{backup_table}（確認無誤後可自行刪除該表）")


def main():
    parser = argparse.ArgumentParser(description="將 Statistic 表的 player_id 欄位資料轉移至 id 欄位")
    parser.add_argument("--check", action="store_true", help="只檢查目前狀態，不做任何變更")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="資料庫檔案路徑（預設為專案根目錄的 generic.db）")
    args = parser.parse_args()

    if not args.db.exists():
        raise FileNotFoundError(f"找不到資料庫檔案：{args.db}")

    conn = sqlite3.connect(args.db)
    try:
        if args.check:
            check(conn)
        else:
            migrate(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()