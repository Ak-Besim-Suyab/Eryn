import random
from dataclasses import dataclass, field, fields
from collections import Counter

@dataclass
class ItemLoot:
    type: str
    id: str
    weight: float = 100
    min: int = 1
    max: int = 1

@dataclass
class ItemOpenAction:
    type: str
    loot: list[ItemLoot] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.loot, list):
            self.loot = [ItemLoot(**loot) for loot in self.loot]

@dataclass(frozen=True)
class ItemFlag:
    openable: bool = False
    consumable: bool = False

    def active(self) -> list[str]:
        return [flag.name for flag in fields(self) if getattr(self, flag.name)]

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
                match action["type"]:
                    case "open":
                        formated_actions.append(ItemOpenAction(**action))
                    case _:
                        raise ValueError(f"不支援的動作類型: {action['type']}")
                    
            self.actions = formated_actions

    def get_action(self, action_type: type):
        return next((action for action in self.actions if isinstance(action, action_type)), None)

    def has_action(self, action_type: type) -> bool:
        return self.get_action(action_type) is not None

    # def roll(self) -> Counter:
    #     entry = random.choices(self.loots, weights=[loot["weight"] for loot in self.loots])[0]

    #     rewards = Counter()
    #     rewards[(entry["type"], entry["id"])] = random.randint(entry["min"], entry["max"])
    #     return rewards