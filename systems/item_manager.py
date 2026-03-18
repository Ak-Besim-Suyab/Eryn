"""
這個物件用來存放物品資料
導入時請導入唯一實例
"""
import json

from pathlib import Path
from cores.logger import logger

ITEM_PATH = "data/items/"

class ItemManager:
    def __init__(self):
        self._items = {}
        self._load()

    def _load(self):
        total_files = 0
        total_items = 0
        folder = Path(ITEM_PATH)

        if not folder.exists():
            raise FileNotFoundError(f"ItemManager | 找不到資料夾: {ITEM_PATH}")

        for file in folder.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    for item in data:
                        item_id = item.get("item_id")
                        if item_id:
                            self._items[item_id] = item

                count = len(data)
                total_files += 1
                total_items += count
                logger.info(f"ItemManager | 載入 {file.name} 成功，總共載入 {count} 個物品")

            except Exception as e:
                logger.error(f"ItemManager | 無法讀取 {file.name}: {e}")

            except json.JSONDecodeError:
                logger.error(f"ItemManager | {file.name} 的 JSON 格式錯誤: {e}")

        logger.info(f"ItemManager | 資料載入完畢，總共載入 {total_files} 個檔案，包含 {total_items} 個物品")
      
    def get_item(self, item_id: str) -> dict:
        item = self._items.get(item_id)
        if item is None:
            raise KeyError(f"ItemManager | 發生錯誤，找不到 {item_id} 物品資料，請確認名稱是否正確，或檔案是否遺失。")
        return item
    
    # def get_items_by_tag(self, tags: list[str] | str) -> dict:
    #     # 根據標籤取得物品列表
    #     if isinstance(tags, str):
    #         tags = [tags]

    #     tags = set(tags)
        
    #     items = {}
    #     for item_name, item_data in self._items.items():
    #         item_tags = set(item_data.get("tags", []))
    #         if tags.issubset(item_tags):
    #             items[item_name] = item_data

    #     return items

item_manager = ItemManager()