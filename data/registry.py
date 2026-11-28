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
    ComponentMap,
    Slot,
    Material, 
    LootTable, 
    Line,
    Race,
    Skill,
)
from data.schema.item_component import COMPONENTS, ItemComponent

from typing import Generic, TypeVar

T = TypeVar("T")

class Storage(Generic[T]):
    def __init__(self, path: str, schema: type[T]):
        self._path = path
        self._schema = schema
        self._storage: dict[str, T] = {}

        self.load()

    def __contains__(self, key) -> bool:
        return key in self._storage

    def load(self):
        raw = file.load_dir(self._path)
        if not raw:
            logger.warning(f"路徑所取得的資料為空: {self._path}")

        self._storage = {name: self._schema(**data) for name, data in raw.items()}

    # 取得單筆資料
    def get(self, name: str) -> T | None:
        obj = self._storage.get(name)
        return deepcopy(obj) if obj else None

class SkillStorage(Storage[Skill]):
    def __init__(self):
        super().__init__("data/skills", Skill)

class RegionStorage(Storage[Region]):
    def __init__(self):
        super().__init__("data/regions", Region)

    def get_all(self) -> list[Region]:
        return [deepcopy(data) for data in self._storage.values()]

class ItemStorage(Storage[Item]):
    def __init__(self):
        super().__init__("data/items", Item)

    def load(self):
        raw = file.load_dir(self._path)
        if not raw:
            logger.warning(f"路徑所取得的資料為空: {self._path}")

        self._storage = {name: self._parse(data) for name, data in raw.items()}

    def _parse(self, data: dict) -> Item:
        """將原始物品資料中的 components 依 COMPONENTS 定義轉換為對應元件"""
        data = data.copy()
        raw_components = data.pop("components", None) or {}
        components = {}

        for key, value in raw_components.items():
            component = COMPONENTS.get(key)
            if component is None:
                raise ValueError(f"不支援的物品元件類型: {key}")

            components[component] = component.component({} if value is None else value)

        return Item(components=ComponentMap(components), **data)

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

    # 取得符合條件的所有資料
    def find(self, component: ItemComponent) -> list[Item]:
        """
        返回包含指定元件的所有物品
        """
        matchs = []
        for data in self._storage.values():
            if data.has(component):
                matchs.append(deepcopy(data))

        return matchs

class SlotStorage(Storage[Slot]):
    def __init__(self):
        super().__init__("data/slots", Slot)

class MaterialStorage(Storage[Material]):
    def __init__(self):
        super().__init__("data/materials", Material)

class ContainerStorage(Storage[Container]):
    def __init__(self):
        super().__init__("data/containers", Container)

class RoleStorage(Storage[Role]):
    def __init__(self):
        super().__init__("data/roles", Role)
    
    def get_all(self) -> list[Role]:
        return [deepcopy(data) for data in self._storage.values()]
    
    # 例如: 找查特定分類時, 填入 (category = "specific_category"), 找查特定標籤時, 填入 (tag = "specific_tag")
    def find(self, **filters) -> list[Role] | None:
        result = [
            deepcopy(data)
            for data in self._storage.values()
            if all(getattr(data, key) == value for key, value in filters.items())
        ]
        return result or None
    
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
SKILLS      = SkillStorage()
REGIONS     = RegionStorage()
ITEMS       = ItemStorage()
SLOTS       = SlotStorage()
MATERIALS   = MaterialStorage()
CONTAINERS  = ContainerStorage()
ROLES       = RoleStorage()
LOOT_TABLES = LootTableStorage()
LINES       = LineStorage()
RACES       = RaceStorage()