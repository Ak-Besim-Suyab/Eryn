from enum import StrEnum, auto

class ResourceName(StrEnum):
    FOOD = auto()
    WOOD = auto()
    STONE = auto()
    IRON = auto()

class CurrencyName(StrEnum):
    VIN = auto()