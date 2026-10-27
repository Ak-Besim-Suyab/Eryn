from dataclasses import dataclass, field, fields

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

    def __post_init__(self):
        if isinstance(self.flags, dict):
            self.flags = ItemFlag(**self.flags)