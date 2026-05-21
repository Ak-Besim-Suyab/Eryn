from dataclasses import dataclass

@dataclass
class Item:
    id: str
    type: str = "generic"
    name: str = "未知物品"
    description: str = "沒有有關描述。"
    emoji: str = "📦"
    price: int = 1

@dataclass
class Weapon(Item):
    attack_power: int = 0