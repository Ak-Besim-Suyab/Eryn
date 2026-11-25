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

class Outcome(StrEnum):
    CRITICAL_FAILURE = auto()
    FAILURE          = auto()
    SUCCESS          = auto()
    CRITICAL_SUCCESS = auto()