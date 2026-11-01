from dataclasses import dataclass, field

RESOURCES = ["wood", "stone", "food"]

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

    def get_leveling_conditions(self, level: int) -> dict[str, int] | None:
        # find condition for current level, return None if it's max level.
        if not any(level_condition.level == level for level_condition in self.level_conditions):
            return None

        return {
            resource: sum(getattr(level_condition, resource) for level_condition in self.level_conditions if level_condition.level <= level)
            for resource in RESOURCES
        }