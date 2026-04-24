"""
這個檔案負責定義戰利品表 (Loot) 以及戰利品管理器 (LootManager)
這裡會對抽取的物品進行驗證，預防無效的物品被回傳
"""
import random
from dataclasses import dataclass, field
from data.type import LootType
from models.item import item_registry
from cores.registry import AssetRegistry
from cores.logger import logger

"""
這裡定義戰利品入口
type: 這裡會指示戰利品類型, 目前只有 item 和 loot 兩種, 執行邏輯時會根據類型調用 item_manager 或 loot_manager 來獲取對應的物件
item: 這裡會指示物品 ID, 調用管理器並傳入以獲得對應物件
min: 掉落物最小值，預設為 1
max: 掉落物最大值，預設為 1
"""

@dataclass
class Entry:
    type: str
    id: str
    weight: int
    min: int = 1
    max: int = 1


@dataclass
class Loot:
    id: str
    entries: list[Entry] = field(default_factory=list)

    def __post_init__(self):
        # 這裡是後處理，把宣告後的物件裡的掉落表 (loots) 轉換成 Loots 類別的實例，然後再放回去
        if self.entries and isinstance(self.entries[0], dict):
            self.entries = [Entry(**entry) for entry in self.entries]


class LootManager(AssetRegistry[Loot]):
    def __init__(self):
        super().__init__(
            model = Loot, 
            path = "assets/loots"
        )
        self.max_depth = 5

    def roll(self, loot_id: str, depth: int = 0) -> dict[str, int]:

        result = {}

        # 這裡是防呆機制，基於朝狀戰利品結構，如果意外讓戰利品陷入遞迴時，超過指定深度會停止執行並回報錯誤。
        if depth > self.max_depth:
            logger.warning(f"掉落表 {loot_id} 的遞迴深度超過限制，可能存在循環引用，需要檢查掉落表，已停止繼續執行。")
            return result

        loot = self.get(loot_id)
        if not loot or not loot.entries:
            return result
 
        weights = [entry.weight for entry in loot.entries]
        if sum(weights) == 0:
            return result
        
        record = random.choices(loot.entries, weights=weights, k=1)[0]

        match record.type:
            case LootType.ITEM:
                # 這裡對物品進行驗證，若出現無效的物品，回報錯誤並跳過處理
                if item_registry.get(record.id) is None:
                    logger.error(f"掉落表 {loot_id} 中的條目 {record.id} 有無效的物品 ID {record.id}, 已跳過。")
                    return result
                
                amount = random.randint(record.min, record.max)
                result[record.id] = result.get(record.id, 0) + amount
                
            case LootType.LOOT:
                nested_result = self.roll(record.id, depth + 1)

                for item_id, amount in nested_result.items():
                    result[item_id] = result.get(item_id, 0) + amount
            case _:
                logger.error(f"掉落表 {loot_id} 中的條目 {record.id} 有無效的類型 {record.type}, 已跳過。")

        return result

# 建立唯一實例
loot_manager = LootManager()
