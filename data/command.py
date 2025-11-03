from enum import Enum

class CommandType(str, Enum):
    LOOK = "look"
    HOME = "home"
    COMBAT = "combat"
    EXCAVATE = "excavate"
    TARGET = "target"
    DIALOGUE = "dialogue"
    TAME = "tame"
    RETURN = "return"
    ATTACK = "attack"
    VICTORY = "victory"