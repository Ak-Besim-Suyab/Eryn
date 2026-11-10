""" 此函式庫用於定義資料註冊物件
"""
from copy import deepcopy
from lib.util import file
from cores import logger
from data.schema import (
    Container, 
    Role, 
    Region,
    Item, 
    Slot,
    Resource, 
    Building, 
    LootTable, 
    Line,
    Race,
)
from data.schema.type import ItemType

from typing import Generic, TypeVar

T = TypeVar("T")

class Storage(Generic[T]):
    def __init__(self, path: str, schema: type[T]):
        self._path = path
        self._schema = schema
        self._storage: dict[str, T] = {}

        self._load()

    def _load(self):
        raw = file.load_dir(self._path)
        if not raw:
            logger.warning(f"路徑所取得的資料為空: {self._path}")

        self._storage = {name: self._schema(**data) for name, data in raw.items()}

    # 取得單筆資料
    def get(self, name: str) -> T | None:
        obj = self._storage.get(name)
        return deepcopy(obj) if obj else None
    
class RegionStorage(Storage[Region]):
    def __init__(self):
        super().__init__("data/regions", Region)

class ItemStorage(Storage[Item]):
    def __init__(self):
        super().__init__("data/items", Item)

    def find_tags(self, *tags, match_any: bool = False) -> list[Item]:

        tags = set(tags)
        matchs = []

        for data in self._storage.values():
            item_tags = data.tags

            if match_any:
                find = not tags.isdisjoint(item_tags) # 判斷兩個集合是否有交集, 有共同元素時會返回 False, 這裡要取反
            else:
                find = tags.issubset(item_tags) # 判斷傳入集合是否為物品標籤的子集合

            if find:
                matchs.append(deepcopy(data))

        return matchs

    # 取得符合條件的所有資料, filters 為不定長度位置參數, 可填入多個條件, 參數名稱要對應查詢項目
    def find(self, item_type: ItemType) -> list[Item]:
        """
        返回符合所有條件的物品
        """
        matchs = []
        for data in self._storage.values():
            if data.has_component(item_type):
                matchs.append(deepcopy(data))

        return matchs

class SlotStorage(Storage[Slot]):
    def __init__(self):
        super().__init__("data/slots", Slot)

class ResourceStorage(Storage[Resource]):
    def __init__(self):
        super().__init__("data/resources", Resource)

class ContainerStorage(Storage[Container]):
    def __init__(self):
        super().__init__("data/containers", Container)

class RoleStorage(Storage[Role]):
    def __init__(self):
        super().__init__("data/roles", Role)
    
    def get_all(self) -> list[Role]:
        return [deepcopy(data) for data in self._storage.values()]
    
    # 例如: 找查特定分類時, 填入 (category = "specific_category"), 找查特定標籤時, 填入 (tag = "specific_tag")
    def find(self, **filters) -> list[Role]:
        return [deepcopy(data) for data in self._storage.values() if all(getattr(data, key) == value for key, value in filters.items())]

class BuildingStorage(Storage[Building]):
    def __init__(self):
        super().__init__("data/buildings", Building)
    
class LootTableStorage(Storage[LootTable]):
    def __init__(self):
        super().__init__("data/loot_tables", LootTable)

class LineStorage(Storage[Line]):
    def __init__(self):
        super().__init__("data/lines", Line)

class RaceStorage(Storage[Race]):
    def __init__(self):
        super().__init__("data/races", Race)

# ----
# 註冊資料物件, 讓其他函式庫可以直接導入使用
# ----
REGIONS     = RegionStorage()
ITEMS       = ItemStorage()
SLOTS       = SlotStorage()
RESOURCES   = ResourceStorage()
CONTAINERS  = ContainerStorage()
ROLES       = RoleStorage()
BUILDINGS   = BuildingStorage()
LOOT_TABLES = LootTableStorage()
LINES       = LineStorage()
RACES       = RaceStorage()