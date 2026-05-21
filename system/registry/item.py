from cores.registry import AssetRegistry

from game.model import Item, Weapon

model = {
    "item": Item,
    "weapon": Weapon
}

class ItemRegistry(AssetRegistry):
    def __init__(self):
        super().__init__(path = "assets/items")

    def get(self, item_id: str):
        """
        該方法嘗試獲取物品資料
        """
        data = self._data.get(item_id)
        if not data:
            return None
        
        item_type = data.get("type", "item")
        item_model = model.get(item_type)

        return item_model(**data)

# singleton declaration.
item_registry = ItemRegistry()
