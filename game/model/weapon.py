from dataclasses import dataclass

from .item import Item

@dataclass
class Weapon(Item):
    damage: int = 0