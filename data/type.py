from enum import Enum

class Type(str, Enum):
    ...

class LootType(str, Enum):
    ITEM = "item"
    LOOT = "loot"

class ActionType(Type):
    MINING = "mining"
    FISHING = "fishing"
    GARDENING = "gardening"
    STEALING = "stealing"
    MOURNING = "mourning"

class StatusType(str, Enum):
    UNLUCKY = "unlucky"
    TWIST_OF_FATE = "twist_of_fate"

class TitleType(str, Enum):
    DEFAULT = "default"
    PLAYER = "player"
    BOT = "bot"

class ColorType(str, Enum):
    GOLD = "gold"
    DARK_GOLD = "dark_gold"