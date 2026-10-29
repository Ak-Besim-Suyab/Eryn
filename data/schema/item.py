import random
from collections import Counter
from enum import StrEnum
from dataclasses import dataclass, field

class ActionType(StrEnum):
    OPEN = "openable"
    CONSUME = "consumable"

@dataclass
class ItemLoot:
    type: str
    id: str
    weight: float = 100
    min: int = 1
    max: int = 1

@dataclass
class ItemConsume:
    type: str = ActionType.CONSUME

@dataclass
class ItemOpen:
    type: str = ActionType.OPEN
    loot: list[ItemLoot] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.loot, list):
            self.loot = [ItemLoot(**loot) for loot in self.loot]

    def roll(self, times: int = 1) -> Counter:
        rewards = Counter()
        for _ in range(times):
            entry = random.choices(self.loot, weights = [loot.weight for loot in self.loot])[0]
            rewards[(entry.id, entry.type)] += random.randint(entry.min, entry.max)

        return rewards

@dataclass
class ItemFlag:
    openable: bool = False
    consumable: bool = False

ACTION_TYPES = {
    ActionType.OPEN: ItemOpen,
    ActionType.CONSUME: ItemConsume,
}

@dataclass
class Item:
    id: str
    name: str = "未知物品"
    description: str = "沒有任何描述。"
    emoji: str = "📦"
    flags: ItemFlag = field(default_factory=ItemFlag)
    actions: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.flags, dict):
            self.flags = ItemFlag(**self.flags)

        if isinstance(self.actions, list):

            formated_actions = []
            for action in self.actions:
                cls = ACTION_TYPES.get(action["type"])
                if cls is None:
                    raise ValueError(f"不支援的動作類型: {action['type']}")

                formated_actions.append(cls(**action))
                    
            self.actions = formated_actions

    def get_action(self, action_type: str):
        return next((action for action in self.actions if action.type == action_type), None)

    def has_action(self, action_type: str) -> bool:
        return self.get_action(action_type) is not None

    def is_openable(self) -> bool:
        return self.has_action(ActionType.OPEN)

    def is_consumable(self) -> bool:
        return self.has_action(ActionType.CONSUME)