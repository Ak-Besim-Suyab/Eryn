from enum import Enum

class LootType(str, Enum):
    ITEM = "item"
    LOOT = "loot"

class SkillType(str, Enum):
    MINING = "mining"
    FISHING = "fishing"
    GARDENING = "gardening"

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