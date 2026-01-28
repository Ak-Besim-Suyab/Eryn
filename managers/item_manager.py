
from utils.logger import logger
import json
from pathlib import Path

ITEM_PATH = "data/items/"

class ItemManager:
    def __init__(self):
        self._items = {}
        self._load_all_items()

    def _load_all_items(self):
        # load all item json files from ITEM_PATH
        folder = Path(ITEM_PATH)

        # check if folder exists
        if not folder.exists():
            raise FileNotFoundError(f"找不到資料夾: {ITEM_PATH}")

        # load all json files in the folder
        total_files = 0
        total_items = 0
        for file in folder.glob("*.json"):
            try:
                count = self._load_file(file)
                total_files += 1
                total_items += count
                logger.info(f"載入 {file.name} 成功，總共載入 {count} 個物品")
            except Exception as e:
                logger.error(f"無法讀取 {file.name}: {e}")

        logger.info(f"Item 資料載入完畢，總共載入 {total_files} 個檔案，包含 {total_items} 個物品")

    def _load_file(self, file_path: str):
        # 載入單個 JSON 檔案中的物品資料
        count = 0

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, dict):
                for item_id, item_data in data.items():
                    self._items[item_id] = item_data
                    count += 1
            else:
                logger.warning(f"Item 資料 {file_path} 不包含有效的物品字典。")

        return count
      
    def get_item(self, item_id: str) -> dict:
        # 透過 item_id 取得物品資料
        return self._items.get(item_id)
    
    def get_items_by_tag(self, tag: str) -> list:
        # 根據標籤取得物品列表
        items = {}
        for item_name, item_data in self._items.items():
            if tag in item_data.get("tags", []):
                items[item_name] = item_data
        return items