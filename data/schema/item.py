from enum import StrEnum
from dataclasses import dataclass, field

class ActionType(StrEnum):
    LOOT = "loot"
    FOOD = "food"

@dataclass
class FoodItem:
    type: str = ActionType.FOOD

@dataclass
class LootItem:
    type: str = ActionType.LOOT
    loot_tables: list[str] = field(default_factory=list)
            
ACTION_TYPES = {
    ActionType.LOOT: LootItem,
    ActionType.FOOD: FoodItem,
}

@dataclass
class Item:
    id: str
    name: str = "未知物品"
    description: str = "沒有任何描述。"
    icon: str = "📦"
    components: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.components, list):
            formated_components = []
            for component in self.components:
                cls = ACTION_TYPES.get(component['type'])
                if cls is None:
                    raise ValueError(f"不支援的組件類型: {component['type']}")

                formated_components.append(cls(**component))
                    
            self.components = formated_components

    def get_component(self, component_type: str):
        return next((component for component in self.components if component.type == component_type), None)

    def has_component(self, component_type: str) -> bool:
        return self.get_component(component_type) is not None

    def is_lootable(self) -> bool:
        return self.has_component(ActionType.LOOT)

    def is_consumable(self) -> bool:
        return self.has_component(ActionType.FOOD)