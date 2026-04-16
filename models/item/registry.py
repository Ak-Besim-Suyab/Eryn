"""
這個檔案負責定義物品 (Item) 以及物品管理器 (ItemManager)
"""
from dataclasses import dataclass
from cores.registry import Registry

@dataclass
class Item:
    id: str
    name: str = "未知物品"
    description: str = "沒有任何有關描述。"
    image: str = "📦"
    price: int = 1

class ItemReigstry(Registry[Item]):
    def __init__(self):
        super().__init__(
            model = Item, 
            path = "assets/items"
        )

# 建立唯一實例
item_registry = ItemReigstry()
