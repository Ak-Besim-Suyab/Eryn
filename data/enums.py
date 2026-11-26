from enum import StrEnum, auto

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

class Outcome(StrEnum):
    CRITICAL_FAILURE = auto()
    FAILURE          = auto()
    SUCCESS          = auto()
    CRITICAL_SUCCESS = auto()