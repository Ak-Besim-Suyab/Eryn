from dataclasses import dataclass, field

@dataclass
class LevelConditions:
    level: int
    wood: int
    stone: int
    food: int

@dataclass
class Building:
    level_conditions: list[LevelConditions] = field(default_factory=list)

    def __post_init__(self):
        if self.level_conditions and isinstance(self.level_conditions, list) and isinstance(self.level_conditions[0], dict):
            self.level_conditions = [LevelConditions(**level) for level in self.level_conditions]