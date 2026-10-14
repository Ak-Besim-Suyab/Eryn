"""
統計活躍度未達標的成員。

篩選條件 (全部同時成立)：
- Statistic.total_voice_time    累計語音時間為 0
- Statistic.total_daily_claims  累計簽到天數為 0
- Statistic.total_message_send  累計發送訊息數為 0
- Player.level                  等級為 1
- Player.experience             經驗值未達升到 2 級所需的經驗量

使用方式 (在專案根目錄執行)：
    python scripts/inactive_members.py
"""
import sys
from pathlib import Path

# 讓腳本不論從哪個目錄執行，都能 import 到專案根目錄的 database / models
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from database import db
from models.player import Player
from models.statistic import Statistic


def get_inactive_stats():
    # 1 級升 2 級所需的經驗量，直接沿用 Player 的公式，避免數值不同步
    required_exp = Player.get_required_exp(1)

    # Statistic 與 Player 沒有外鍵，但兩者的 id 都是 Discord 使用者 ID，手動指定 join 條件
    return (
        Statistic.select(Statistic, Player)
        .join(Player, on=(Statistic.id == Player.id), attr="player")
        .where(
            (Statistic.total_voice_time == 0)
            & (Statistic.total_daily_claims == 0)
            & (Statistic.total_message_send == 0)
            & (Player.level == 1)
            & (Player.experience < required_exp)
        )
        .order_by(Statistic.id)
    )


def main():
    db.connect(reuse_if_open=True)
    try:
        total = Statistic.select().count()
        inactive = list(get_inactive_stats())

        print(f"資料庫共 {total} 筆統計資料，其中 {len(inactive)} 筆活躍度未達標")
        print("-" * 40)

        if not inactive:
            print("沒有符合條件的成員。")
            return

        for stat in inactive:
            player = stat.player
            # display_name 目前不會被自動更新，ID 才是可靠的識別依據
            print(
                f"{stat.id} | {stat.display_name} | "
                f"Lv.{player.level} | Exp {player.experience}"
            )
    finally:
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    main()
