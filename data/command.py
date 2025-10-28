from enum import Enum

class CommandType(Enum):
    LOOK = "look"
    HOME = "home"
    COMBAT = "combat"
    EXCAVATE = "excavate"
    TARGET = "target"