"""
這個檔案負責定義戰利品表 (Loot) 以及戰利品管理器 (LootManager)
"""
import random
from dataclasses import dataclass, field
from models.type import LootType
from cores.loader import JsonLoader
from cores.logger import logger

loot_path = "assets/loots"

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


class LootManager:
    def __init__(self):
        self._loots: dict[str, Loot] = {}
        self._load()

    def _load(self):
        raw_data = JsonLoader.load(loot_path)

        # 檢查資料是否有被讀取
        if not raw_data:
            logger.error(f"找不到資料夾: {loot_path}")
            return
        
        total_files = 0
        
        for filename, data in raw_data.items():

            # 檢查資料格式是否正確
            if not isinstance(data, dict):
                logger.error(f"{filename} 的 JSON 格式出現錯誤")
                continue
            
            try:
                loot = Loot(**data)
                self._loots[loot.id] = loot
                total_files += 1
                logger.info(f"載入 {filename}.json 檔案成功")

            except TypeError as e:
                logger.error(f"{filename} 的 JSON 格式與 Loot 類別不相容: {e}")
                continue
        
        logger.info(f"資料載入完畢，總共載入 {total_files} 個檔案")

    def get_loot(self, loot_id: str) -> Loot | None:
        return self._loots.get(loot_id)

    def get_all_loots(self) -> list[Loot]:
        return list(self._loots.values())


    def roll(self, loot_id: str, depth: int = 0) -> dict[str, int]:

        result = {}

        if depth > 5:
            logger.warning(f"掉落表 {loot_id} 的遞迴深度超過限制，可能存在循環引用，需要檢查掉落表，已停止繼續執行。")
            return result

        loot = self.get_loot(loot_id)
        if not loot or not loot.entries:
            return result
 
        weights = [entry.weight for entry in loot.entries]
        if sum(weights) == 0:
            return result
        
        record = random.choices(loot.entries, weights=weights, k=1)[0]

        match record.type:
            case LootType.ITEM:
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
