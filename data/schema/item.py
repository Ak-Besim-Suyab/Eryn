from enum import StrEnum
from dataclasses import dataclass, field

class ItemType(StrEnum):
    LOOT = "loot"
    FOOD = "food"
    EQUIPMENT = "equipment"

@dataclass(frozen=True)
class Affix:
    id: str
    type: str
    value: int

@dataclass
class FoodItem:
    type: str = ItemType.FOOD

@dataclass
class LootItem:
    type: str = ItemType.LOOT
    loot_tables: list[str] | None = field(default_factory=list)

@dataclass
class EquipmentItem:
    type: str = ItemType.EQUIPMENT
    slot: str = None
    affixes: list[Affix] | None = field(default_factory=list)

    def __post_init__(self):
        if self.affixes and isinstance(self.affixes, list):
            self.affixes = [Affix(**affix) for affix in self.affixes]

    def get_affix(self, id: str = None, type: str = None) -> Affix | None:
        """
        返回符合條件的詞綴, 可以傳入 id 或 type, 會返回符合所有條件的詞綴
        """
        if id and type:
            return next((affix for affix in self.affixes if affix.id == id and affix.type == type), None)
        if id:
            return next((affix for affix in self.affixes if affix.id == id), None)
        if type:
            return next((affix for affix in self.affixes if affix.type == type), None)
            
ACTION_TYPES = {
    ItemType.LOOT: LootItem,
    ItemType.FOOD: FoodItem,
    ItemType.EQUIPMENT: EquipmentItem,
}

@dataclass
class Item:
    id: str
    name: str = "未知物品"
    description: str = "沒有任何描述。"
    tooltip: str = "無。"
    icon: str = "📦"
    components: list[dict] | None = field(default_factory=list)

    def __post_init__(self):
        if self.components and isinstance(self.components, list):
            formated_components = []
            for component in self.components:
                cls = ACTION_TYPES.get(component['type'])
                if cls is None:
                    raise ValueError(f"不支援的組件類型: {component['type']}")

                formated_components.append(cls(**component))
                    
            self.components = formated_components

    def get_component(self, component_type: str) :
        return next((component for component in self.components if component.type == component_type), None)

    def has_component(self, component_type: str) -> bool:
        return self.get_component(component_type) is not None

    def is_lootable(self) -> bool:
        return self.has_component(ItemType.LOOT)

    def is_consumable(self) -> bool:
        return self.has_component(ItemType.FOOD)

    def is_equippable(self) -> bool:
        return self.has_component(ItemType.EQUIPMENT)