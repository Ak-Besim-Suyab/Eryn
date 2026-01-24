from utils.logger import logger
from context import Context

class Item:
    def __init__(self, item_id: str, name: str,tags: list, base_value: int = 0):
        self.item_id = item_id
        self.name = name
        self.tags = tags
        self.base_value = base_value

class ItemManager:
    def __init__(self):
        self.items = {}
    
    def register_all(self):
        item_datas = Context.json_loader.load("data/items.json")
        logger.info(f"[物品] 載入 {len(item_datas)} 個物品")

        for item_id, item_data in item_datas.items():
            item_obj = Item(
                item_id=item_id,
                name=item_data['name'],
                tags=item_data.get('tags', []),
                base_value=item_data.get('base_value', 0)
            )
            self.items[item_id] = item_obj

    def get_item(self, item_id: str) -> Item:
        return self.items.get(item_id)
    
    def get_all(self) -> list:
        return list(self.items.values())