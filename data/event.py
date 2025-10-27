from enum import Enum

class EventType(Enum):
    OBTAIN_ITEM = "obtain_item"
    OBTAIN_EXPERIENCE = "obtain_experience"

    FIND_ENTITY = "find_entity"

    LEVEL_UP = "level_up"