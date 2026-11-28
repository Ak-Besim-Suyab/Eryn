from enum import IntEnum, StrEnum, auto

class MaterialName(StrEnum):
    FOOD  = auto()
    WOOD  = auto()
    STONE = auto()
    IRON  = auto()

class CurrencyName(StrEnum):
    VIN = auto()

class BuildingName(StrEnum):
    SANCTUARY = auto()

class AttributeName(StrEnum):
    STRENGTH     = auto()
    CONSTITUTION = auto()
    DEXTERITY    = auto()
    PERCEPTION   = auto()
    INTELLIGENCE = auto()
    CHARISMA     = auto()
    LUCK         = auto()
    SANITY       = auto()
    KARMA        = auto()

class Outcome(IntEnum):
    CRITICAL_FAILURE = 0
    FAILURE          = 1
    SUCCESS          = 2
    CRITICAL_SUCCESS = 3

    @ property
    def label(self) -> str:
        return {
            self.CRITICAL_FAILURE : "大失敗",
            self.FAILURE          : "失敗",
            self.SUCCESS          : "成功",
            self.CRITICAL_SUCCESS : "大成功",
        }[self]