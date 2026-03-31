"""
這個檔案負責定義物品 (Item) 以及物品管理器 (ItemManager)
"""

from dataclasses import dataclass
from cores.loader import JsonLoader
from cores.logger import logger

item_path = "assets/items"

@dataclass
class Item:
    id: str
    name: str = "未知物品"
    description: str = "沒有任何有關描述。"

    def use(self):
        # 這裡會定義使用物品時的邏輯
        pass


class ItemManager:
    def __init__(self):
        self._items: dict[str, Item] = {}
        self._load()

    def _load(self):
        raw_data = JsonLoader.load(item_path)

        # 檢查資料是否有被讀取
        if not raw_data:
            logger.error(f"ItemManager | 找不到資料夾: {item_path}")
            return
        
        total_files = 0
        
        for filename, data in raw_data.items():

            # 檢查資料格式是否正確
            if not isinstance(data, dict):
                logger.error(f"ItemManager | {filename} 的 JSON 格式錯誤")
                continue
            
            try:
                item = Item(**data)
                self._items[item.id] = item
                total_files += 1
                logger.info(f"ItemManager | 載入 {filename}.json 檔案成功")

            except TypeError as e:
                logger.error(f"ItemManager | {filename} 的 JSON 格式與 Item 類別不相容: {e}")
                continue
        
        logger.info(f"ItemManager | 資料載入完畢，總共載入 {total_files} 個檔案")

    def get_item(self, item_id: str) -> Item | None:
        return self._items.get(item_id)

    def get_all_items(self) -> list[Item]:
        return list(self._items.values())

# 建立唯一實例
item_manager = ItemManager()
