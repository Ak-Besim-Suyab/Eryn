from dataclasses import dataclass, field

@dataclass(frozen=True)
class ItemFlag:
    openable: bool = False
    consumable: bool = False

@dataclass
class Item:
    id: str
    name: str = "未知物品"
    description: str = "沒有任何描述。"
    emoji: str = "📦"
    flags: ItemFlag = field(default_factory=ItemFlag)

    def __post_init__(self):
        if isinstance(self.flags, dict):
            self.flags = ItemFlag(**self.flags)